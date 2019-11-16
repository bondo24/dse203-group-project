#!/usr/bin/env python3

# for configuration management
import yaml

# open config yaml file
with open('config.yml', 'r') as config_yaml:
    config = yaml.load(config_yaml, Loader=yaml.BaseLoader)

# used just for human readable json
import json

# scraping
from company_scraper import scrape

output = scrape()

# generate neo4j graph
from neo4j import GraphGenerator

graph_generator = GraphGenerator(config['neo4j'])
graph_generator.create_graph(output['parent_company'])
graph_generator.create_relationships(output['acquisitions'])


from wordcloud_generator import generate_wordcloud

generate_wordcloud(output)

# just for debugging
print(json.dumps(output["parent_company"], indent=4))
print(json.dumps(output["competitors"], indent=4))
