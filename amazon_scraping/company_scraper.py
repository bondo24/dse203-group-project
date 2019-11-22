import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging


from amazon_scraping.spiders.parent_company import ParentCompanySpider
from amazon_scraping.spiders.acquisitions import AcquisitionsSpider
from amazon_scraping.spiders.competitors import CompetitorsSpider
from amazon_scraping.spiders.naics_code import NaicsCodeSpider
from scrapy.utils.project import get_project_settings


def scrape():
    scrapy_settings = get_project_settings()
    # modify scrapy_settings here if needed

    output = {
              "parent_company": {},
              "acquisitions": {},
              "competitors": {}
             }
    configure_logging()
    runner = CrawlerRunner(settings=scrapy_settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(ParentCompanySpider, output=output)
        yield runner.crawl(AcquisitionsSpider, output=output)
        yield runner.crawl(CompetitorsSpider, output=output)
        yield runner.crawl(NaicsCodeSpider, output=output)
        reactor.stop()
    crawl()
    reactor.run()
    return output
