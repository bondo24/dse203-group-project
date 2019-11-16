import scrapy
import re
import pandas as pd

class CompetitorsSpider(scrapy.Spider):

    name = 'competitors'

    first_url = 'https://en.wikipedia.org/wiki/'
    competitions = ['Netflix', 'Fedex', 'Etsy']
    urlsss = []
    for c in competitions:
        urlsss.append(str(first_url + c ))

    start_urls = urlsss

    def parse(self, response):
        title = response.xpath('//*[@id="firstHeading"]/text()').get()
        # get infobox
        infobox_xpath = response.xpath('//*[@id="mw-content-text"]/div/table[*][@class="infobox vcard"]')
        self.output['competitors'][title] = {}
        competitor = self.output['competitors'][title]
        competitor['organization'] = infobox_xpath.xpath('./caption/text()').get()

        if competitor['organization'] == 'Etsy':
            competitor['founded'] = re.sub(r'[^\x00-\x7F]+',' ', infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Launched")]/../td/text()').get())
            competitor['industry'] = infobox_xpath.xpath(
                './tbody/tr[*]/th[contains(text(), "Industry")]/../td[@class="category"]//text()').getall()
            # clean industry values
            competitor['industry'] = list(filter(lambda text: text != '\n', competitor['industry']))

            try:
                competitor['products'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Products")]/ancestor::tr/td/text()').get().split(', ')
            except AttributeError:
                competitor['products'] = None

            except AttributeError:
                competitor['number_of_employees'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Number of employees") or contains(text(), "Employees")]/ancestor::tr/td/text()').get()
                competitor['number_of_employees'] = re.sub('[^0-9]', '', competitor['number_of_employees'])

            except AttributeError:
                competitor['number_of_employees'] = None
                # acquisition['location'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Headquarters")]/ancestor::tr/td/string()').get()
            competitor['summary'] = ''.join(response.xpath('//*[@id="mw-content-text"]/div/p[*]//text()').getall())
            # competitor['number_of_employees']
            line = competitor['summary'].text()
            import re
            match = re.search('(\d+) employees', line)
            if match:
                competitor['number_of_employees'] = match.group(1)



        else:
            competitor['founded'] = re.sub(r'[^\x00-\x7F]+', ' ', infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Founded")]/../td/text()').get())
            competitor['industry'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Industry")]/../td[@class="category"]//text()').getall()
            # clean industry values
            competitor['industry'] = list(filter(lambda text: text != '\n', competitor['industry']))
            # some don't have products
            try:
               competitor['products'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Products")]/ancestor::tr/td/text()').get().split(', ')
            except AttributeError:
                competitor['products'] = None

            except AttributeError:
               competitor['number_of_employees'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Number of employees") or contains(text(), "Employees")]/ancestor::tr/td/text()').get()
               competitor['number_of_employees'] = re.sub('[^0-9]','', competitor['number_of_employees'])
            except AttributeError:
               competitor['number_of_employees'] = None
         # acquisition['location'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Headquarters")]/ancestor::tr/td/string()').get()
            competitor['summary'] = ''.join(response.xpath('//*[@id="mw-content-text"]/div/p[*]/b[contains(text(), "{}")]/..//text()'.format(title)).getall())
