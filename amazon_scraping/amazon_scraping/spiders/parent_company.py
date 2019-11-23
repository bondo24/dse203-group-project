import scrapy
import re
import pandas as pd

class ParentCompanySpider(scrapy.Spider):

    name = 'parent_company'

    start_urls = ['https://en.wikipedia.org/wiki/Amazon_(company)']


    def parse(self, response):
        parent_company = self.output['parent_company']
        title = response.xpath('//*[@id="firstHeading"]/text()').get()
        # get infobox
        infobox_xpath = response.xpath('//*[@id="mw-content-text"]/div/table[*][@class="infobox vcard"]') 

        parent_company['organization'] = infobox_xpath.xpath('./caption/text()').get()
        parent_company['founded'] = re.sub(r'[^\x00-\x7F]+',' ', infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Founded")]/../td/text()').get())
        parent_company['industry'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Industry")]/../td[@class="category"]//text()').getall()
        # clean industry values
        parent_company['industry'] = list(filter(lambda text: text != '\n', parent_company['industry']))
        # some don't have products
        try:
            parent_company['products'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Products")]/ancestor::tr/td//text()').getall()#.split(', ')
        except AttributeError:
            parent_company['products'] = None
        parent_company['number_of_employees'] = infobox_xpath.xpath('./tbody/tr[*]//*[contains(text(), "Number of employees") or contains(text(), "Employees")]/ancestor::tr/td/text()').get().split('(')[0]
        parent_company['number_of_employees'] = re.sub('[^0-9]','', parent_company['number_of_employees'])
        parent_company['location'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Headquarters")]/ancestor::tr/td//@title').get()
        # TODO: right now it only considers a single founder
        parent_company['founder'] = infobox_xpath.xpath('./tbody/tr[*]/th[contains(text(), "Founder") or contains(text(), "Key")]/ancestor::tr/td//text()').get()
        parent_company['summary'] = ''.join(response.xpath('//*[@id="mw-content-text"]/div/p[*]/b[contains(text(), "{}")]/..//text()'.format(parent_company['organization'])).getall())
        parent_company['raw_text'] = ''.join(response.xpath('//*[@id="mw-content-text"]/div/p[*]//text()').getall())
