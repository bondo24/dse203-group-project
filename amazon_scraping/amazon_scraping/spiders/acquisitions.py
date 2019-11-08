import scrapy
import pandas as pd

class AcquisitionsSpider(scrapy.Spider):

    name = 'acquisitions'

    start_urls = ['https://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Amazon']

    def parse(self, response):
        acquisitions_xpath = response.xpath('//*[@id="mw-content-text"]/div/table[1]')[0]
        # only find the ones that have an href
        # competitors_xpath = 
        # for acquisition in acquisitions_xpath.xpath('./tbody/tr[*]/td[2]/a/@href'):
        #     acquisition_page = response.urljoin(acquisition.get())
        #     yield response.follow(acquisition_page, self.parse_acquisition)

        df = pd.read_html(acquisitions_xpath.get(), header=0)[0]
        # df['Acquired for (USD)'] = df['Acquired for (USD)'].replace('[\$,—]', '', regex=True).replace(r'', 0).astype(float)
        # df = df.sort_values(by='Acquired for (USD)', ascending=False)
        df = df.sort_values(by='Used as or integrated with', ascending=False)[:3]

        self.output['acquisitions'] = df

    def parse_acquisition(self, response):
        # yield { 'title': response.xpath('//*[@id="firstHeading"]').get() }
        self.output['acquisitions'].append(response.xpath('//*[@id="firstHeading"]/text()').get())
