#!/usr/bin/env python3

# for configuration management
import yaml

# open config yaml file
with open('config.yml', 'r') as config_yaml:
    config = yaml.load(config_yaml, Loader=yaml.BaseLoader)

# used just for human readable json
import json

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


# scraping
from company_scraper import scrape

output = scrape()

# generate neo4j graph
from neo4j import GraphGenerator

graph_generator = GraphGenerator(config['neo4j'])
graph_generator.create_graph(output['parent_company'])
graph_generator.create_relationships(output['acquisitions'], output['competitors'])
#using stubbed function for now


from text_processing import subject_verb_object_triples


triples = subject_verb_object_triples(output['parent_company']['raw_text'])
graph_generator.create_misc_relationships(triples, output['parent_company']['organization'])
# for t in triples:
#    print(output['parent_company']['organization'], t)

for name, c in output['acquisitions'].items():
    triples = subject_verb_object_triples(c['raw_text'])
    graph_generator.create_misc_relationships(triples, name)

for name, c in output['competitors'].items():
    triples = subject_verb_object_triples(c['raw_text'])
    graph_generator.create_misc_relationships(triples, name)

graph_generator.create_naics_tree()

from wordcloud_generator import generate_wordcloud

generate_wordcloud(output)

from Stanford_PartOfSpeach import stanford_pos
stanford_pos(output)


# just for debugging
print(json.dumps(output["parent_company"], indent=4))
print(json.dumps(output["acquisitions"], indent=4))
print(json.dumps(output["competitors"], indent=4))
