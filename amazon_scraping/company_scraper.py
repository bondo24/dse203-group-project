import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def scrape():
    scrapy_settings = get_project_settings()
    # modify scrapy_settings here if needed

    output = {
              "acquisitions": {},
              "competitors": {}
             }
    process = CrawlerProcess(settings=scrapy_settings)
    process.crawl("acquisitions", output=output)
    process.crawl("competitors", output=output)
    process.start()

    # just for debugging
    return output
