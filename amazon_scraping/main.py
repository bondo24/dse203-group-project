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

# generate neo4j graph
from neo4j import GraphGenerator

graph_generator = GraphGenerator(config['neo4j'])
graph_generator.create_graph()
graph_generator.create_relationships(output['acquisitions'])


from worldcloud_generator import generate_wordcloud

generate_worldcloud(output)

# just for debugging
print(json.dumps(output["competitors"], indent=4))
