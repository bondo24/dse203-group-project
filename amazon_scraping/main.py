#!/usr/bin/env python3

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from amazon_scraping.spiders.acquisitions import AcquisitionsSpider

# used just for human readable json
import json

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
# from amazon_scraping.spiders.acquisitions import AcquisitionsSpider

# used just for human readable json
import json
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop = stopwords.words('english')

import os
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt



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
print(json.dumps(output["competitors"], indent=4))

if not os.path.exists('Figures'):
    os.mkdir('Figures')
text = {}
for j in output:
    for i in output[j]:
        text[i] = output[j][i]['summary'].strip('\n').lower()
        wordcloud = WordCloud().generate(text[i])

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        plt.savefig(os.path.join('Figures', '{}_cloud.jpg'.format(i)), dpi=500)
        # plt.show()