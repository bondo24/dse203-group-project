import scrapy
import re

class NaicsCodeSpider(scrapy.Spider):

    name = 'naics_code'
 
    def generate_naics_url(self, org_name):
        root_url = 'https://siccode.com/business/'
        end_url = re.split(r'\W+', org_name)
        end_url = list(filter(None, end_url))
        return root_url + '-'.join(end_url)

    def start_requests(self):
        urls = []
        urls.append((self.output['parent_company'], self.generate_naics_url(self.output['parent_company']['organization'])))
        for name, company in self.output['acquisitions'].items():
            urls.append((company, self.generate_naics_url(company['organization'])))
        for name, company in self.output['competitors'].items():
            urls.append((company, self.generate_naics_url(company['organization'])))
        for url in urls:
            yield scrapy.Request(url=url[1], callback=self.parse, cb_kwargs={'company': url[0]})

    def parse(self, response, company):
        naics_code = response.xpath('//*[@id="description"]/div[2]/div/div/a[2]/span/text()').get()
        naics_code = int(naics_code.split()[2])
        company['naics_code'] = naics_code
