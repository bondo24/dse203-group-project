#!/usr/bin/env python3

# for configuration management
import yaml

# open config yaml file
with open('config.yml', 'r') as config_yaml:
    config = yaml.load(config_yaml)

# used just for human readable json
import json

# scraping
from company_scraper import scrape

output = scrape()

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop = stopwords.words('english')

import os
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

from neo4j import GraphGenerator

graph_generator = GraphGenerator(config['neo4j'])
graph_generator.create_graph()
graph_generator.create_relationships(output['acquisitions'])

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
