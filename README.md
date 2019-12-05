# Amazon Knowledge Graph
Acquisitions:
- Whole Food Market
- Zappos.com
- Woot

Competitors:
- Netflix
- FedEx
- Etsy

# Install Dependencies
The following has only been tested on Python3.

```
pip install -r requirements.txt
python -m spacy download en
```

# Generating the Knowledge Graph
Running the main.py script will scrape all the information for the Amazon and 3 of its acquisitions and 3 of its competitors from Wikipedia and SICCODE. It will generate a Neo4j graph containing relationships for the companies. It will create a NAICS code tree that connects the corresponding companies together.
```./main.py```
