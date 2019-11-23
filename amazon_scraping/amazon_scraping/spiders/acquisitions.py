import scrapy
import re
import pandas as pd

class AcquisitionsSpider(scrapy.Spider):

    name = 'acquisitions'

    start_urls = ['https://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Amazon']

    def parse(self, response):
        acquisitions_xpath = response.xpath('//*[@id="mw-content-text"]/div/table[1]')[0]
        # only find the ones that have an href
        # for acquisition in acquisitions_xpath.xpath('./tbody/tr[*]/td[2]/a/@href'):
        #     acquisition_page = response.urljoin(acquisition.get())
        #     yield response.follow(acquisition_page, self.parse_acquisition)

        df = pd.read_html(acquisitions_xpath.get(), header=0)[0]
        df['Acquired for (USD)'] = df['Acquired for (USD)'].replace('[\$,—]', '', regex=True).replace(r'', 0).astype(float)
        # convert date str to date format
        df = df.sort_values(by='Used as or integrated with', ascending=False)[:3]
        # company_number = df['Number']
        # for n in company_number.values:
        for index, row in df.iterrows():
            name = row['Company']
            self.output['acquisitions'][name] = {}
            acquisition = self.output['acquisitions'][name]

            acquisition['acquired_on'] = row['Acquired on']
            acquisition['acquired_for'] = row['Acquired for (USD)']
            acquisition_href = acquisitions_xpath.xpath("./tbody/tr[{}]/td[6]/a/@href".format(row['Number']+1))
            yield response.follow(response.urljoin(acquisition_href.get()), self.parse_acquisition, cb_kwargs={'acquisition': acquisition})

    def parse_acquisition(self, response, acquisition):
        title = response.xpath('//*[@id="firstHeading"]/text()').get()
        # get infobox
        infobox_xpath = response.xpath('//*[@id="mw-content-text"]/div/table[*][@class="infobox vcard"]') 

        acquisition['organization'] = infobox_xpath.xpath('./caption/text()').get()
        acquisition['founded'] = re.sub(r'[^\x00-\x7F]+',' ', infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Founded")]/../td/text()').get())
        acquisition['industry'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Industry")]/../td[@class="category"]//text()').getall()
        # clean industry values
        acquisition['industry'] = list(filter(lambda text: text != '\n', acquisition['industry']))
        # some don't have products
        try:
            acquisition['products'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Products")]/ancestor::tr/td/text()').get().split(', ')
        except AttributeError:
            acquisition['products'] = None
        acquisition['number_of_employees'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Number of employees") or contains(text(), "Employees")]/ancestor::tr/td/text()').get()
        acquisition['number_of_employees'] = re.sub('[^0-9]','', acquisition['number_of_employees'])
        acquisition['location'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Headquarters")]/ancestor::tr/td//@title').get()
        # TODO: right now it only considers a single founder
        acquisition['founder'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Founder") or contains(text(), "Key")]/ancestor::tr/td//text()').get()
        acquisition['summary'] = ''.join(response.xpath('//*[@id="mw-content-text"]/div/p[*]/b[contains(text(), "{}")]/..//text()'.format(title)).getall())
        acquisition['raw_text'] = ''.join(response.xpath('//*[@id="mw-content-text"]/div/p[*]//text()').getall())
