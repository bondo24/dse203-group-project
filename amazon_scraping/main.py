#!/usr/bin/env python3

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# for configuration management
import yaml

# open config yaml file
with open('config.yml', 'r') as config_yaml:
    config = yaml.load(config_yaml)
# set default values if they don't exist
neo4j_config = config.get('neo4j', {})
neo4j_config['host'] = neo4j_config.get('host', 'localhost')
neo4j_config['bolt_port'] = neo4j_config.get('bolt_port', 7687)
neo4j_config['user'] = neo4j_config.get('user', 'neo4j')
neo4j_config['password'] = neo4j_config.get('password', 'password')

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd

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
print(json.dumps(output["acquisitions"], indent=4))


from py2neo import Graph, Node, Relationship
graph = Graph(**neo4j_config)

# hard coding amazon for now...
amz_node = Node('company', title='Amazon')
merged_by = Relationship.type('MergedBy')
for company, value in output['acquisitions'].items():
    node = Node('company',
                title=company,
                acquired_on=value['acquired_on'],
                acquired_for=value['acquired_for'],
                organization=value['organization'],
                founded=value['founded'],
                industry=value['industry'],
                products=value['products'],
                number_of_employees=value['number_of_employees'],
                location=value['location'],
                founder=value['founder'],
                summary=value['summary'],
                )
    graph.create(node)
    graph.merge(merged_by(node, amz_node), 'company', 'title')

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
