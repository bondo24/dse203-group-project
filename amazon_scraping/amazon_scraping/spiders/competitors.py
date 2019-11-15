import scrapy
import re
import pandas as pd

class CompetitorsSpider(scrapy.Spider):

    name = 'competitors'

    # competition = ['Netflix', 'Fedex', 'Etsy']
    # competition = ['Netflix', 'Fedex', 'Etsy']
    # df = pd.DataFrame()
    # se = pd.Series(competition)
    # df['competitor'] = se.values
    first_url = 'https://en.wikipedia.org/wiki/'
    competitions = ['Netflix', 'Fedex', 'Etsy']
    urlsss = []
    for c in competitions:
        urlsss.append(str(first_url + c ))

    start_urls = urlsss


    # start_urls = ['https://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Amazon']

    # def parse(self, response):
    #     competitors_xpath = response.xpath('//*[@id="mw-content-text"]/div/table[1]')[0]
    #     competition = ['Netflix', 'Fedex', 'Etsy']
    #     df = pd.DataFrame()
    #     se = pd.Series(competition)
    #     df['Company'] = se.values
    #     # only find the ones that have an href
    #     # for acquisition in acquisitions_xpath.xpath('./tbody/tr[*]/td[2]/a/@href'):
    #     #     acquisition_page = response.urljoin(acquisition.get())
    #     #     yield response.follow(acquisition_page, self.parse_acquisition)
    #
    #     # df = pd.read_html(competitors_xpath.get(), header=0)[0]
    #     # df['Acquired for (USD)'] = df['Acquired for (USD)'].replace('[\$,—]', '', regex=True).replace(r'', 0).astype(float)
    #     # convert date str to date format
    #     # df = df.sort_values(by='Used as or integrated with', ascending=False)[:3]
    #     # company_number = df['Number']
    #     # for n in company_number.values:
    #     for index, row in df.iterrows():
    #         name = row['Company']
    #         self.output['competitor'][name] = {}
    #         competitor = self.output['competitor'][name]
    #
    #
    #         # competitor_href = competitors_xpath.xpath("./tbody/tr[{}]/td[6]/a/@href".format(row['Number']+1))
    #         yield response.follow(response.urljoin("https://en.wikipedia.org/wiki/"), self.parse_competitor, cb_kwargs={'competitor': competitor})

    def parse(self, response):
        title = response.xpath('//*[@id="firstHeading"]/text()').get()
        # get infobox
        infobox_xpath = response.xpath('//*[@id="mw-content-text"]/div/table[*][@class="infobox vcard"]')
        self.output['competitors'][title] = {}
        competitor = self.output['competitors'][title]
        competitor['organization'] = infobox_xpath.xpath('./caption/text()').get()
        competitor['founded'] = re.sub(r'[^\x00-\x7F]+',' ', infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Founded")]/../td/text()').get())
        competitor['industry'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Industry")]/../td[@class="category"]//text()').getall()
        # clean industry values
        competitor['industry'] = list(filter(lambda text: text != '\n', competitor['industry']))
        # some don't have products
        try:
            competitor['products'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Products")]/ancestor::tr/td/text()').get().split(', ')
        except AttributeError:
            competitor['products'] = None
        competitor['number_of_employees'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Number of employees") or contains(text(), "Employees")]/ancestor::tr/td/text()').get()
        competitor['number_of_employees'] = re.sub('[^0-9]','', competitor['number_of_employees'])
        # acquisition['location'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Headquarters")]/ancestor::tr/td/string()').get()
        competitor['summary'] = ''.join(response.xpath('//*[@id="mw-content-text"]/div/p[*]/b[contains(text(), "{}")]/..//text()'.format(title)).getall())
