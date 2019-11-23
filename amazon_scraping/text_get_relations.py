import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')

from spacy.matcher import Matcher
from tqdm import tqdm

pd.set_option('display.max_colwidth', 200)
# %matplotlib inline




text_amazon = """
Amazon.com, Inc.[6] (/ˈæməzɒn/), is an American multinational technology company based in Seattle, Washington, that focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence. It is considered one of the Big Four technology companies along with Google, Apple, and Facebook.[7][8][9]

Amazon is known for its disruption of well-established industries through technological innovation and mass scale.[10][11][12] It is the world's largest e-commerce marketplace, AI assistant provider, and cloud computing platform[13] as measured by revenue and market capitalization.[14] Amazon is the largest Internet company by revenue in the world.[15] It is the second largest private employer in the United States[16] and one of the world's most valuable companies. Amazon is the second largest technology company by revenue.

Amazon was founded by Jeff Bezos on July 5, 1994, in Bellevue, Washington. The company initially started as an online marketplace for books but later expanded to sell electronics, software, video games, apparel, furniture, food, toys, and jewelry. In 2015, Amazon surpassed Walmart as the most valuable retailer in the United States by market capitalization.[17] In 2017, Amazon acquired Whole Foods Market for $13.4 billion, which vastly increased Amazon's presence as a brick-and-mortar retailer.[18] In 2018, Bezos announced that its two-day delivery service, Amazon Prime, had surpassed 100 million subscribers worldwide.[19][20]

Amazon distributes downloads and streaming of video, music, audiobook through its Amazon Prime Video, Amazon Music, and Audible subsidiaries. Amazon also has a publishing arm, Amazon Publishing, a film and television studio, Amazon Studios, and a cloud computing subsidiary, Amazon Web Services. It produces consumer electronics including Kindle e-readers, Fire tablets, Fire TV, and Echo devices. In addition, Amazon subsidiaries include Ring, Twitch.tv, Whole Foods Market, and IMDb. Among various controversies, the company has been criticized for technological surveillance overreach,[21] a hyper-competitive and demanding work culture,[22] tax avoidance,[23] and anti-competitive practices.[24]

In 1994, Jeff Bezos incorporated Amazon. He chose the location Seattle because of technical talent as Microsoft is located there.[25] In May 1997, the organization went public. The company began selling music and videos in 1998, at which time it began operations internationally by acquiring online sellers of books in United Kingdom and Germany. The following year, the organization also sold video games, consumer electronics, home-improvement items, software, games, and toys in addition to other items.

In 2002, the corporation started Amazon Web Services (AWS), which provided data on Web site popularity, Internet traffic patterns and other statistics for marketers and developers. In 2006, the organization grew its AWS portfolio when Elastic Compute Cloud (EC2), which rents computer processing power as well as Simple Storage Service (S3), that rents data storage via the Internet, were made available. That same year, the company started Fulfillment by Amazon which managed the inventory of individuals and small companies selling their belongings through the company internet site. In 2012, Amazon bought Kiva Systems to automate its inventory-management business, purchasing Whole Foods Market supermarket chain five years later in 2017.[26]

In 2000, U.S. toy retailer Toys "R" Us entered into a 10-year agreement with Amazon, valued at $50 million per year plus a cut of sales, under which Toys "R" Us would be the exclusive supplier of toys and baby products on the service, and the chain's website would redirect to Amazon's Toys & Games category. In 2004, Toys "R" Us sued Amazon, claiming that because of a perceived lack of variety in Toys "R" Us stock, Amazon had knowingly allowed third-party sellers to offer items on the service in categories that Toys "R" Us had been granted exclusivity. In 2006, a court ruled in favor of Toys "R" Us, giving it the right to unwind its agreement with Amazon and establish its own independent e-commerce website. The company was later awarded $51 million in damages.[28][29][30]

In 2001, Amazon entered into a similar agreement with Borders Group, under which Amazon would comanage Borders.com as a co-branded service.[31] Borders pulled out of the arrangement in 2007, with plans to also launch its own online store.[32]

On October 18, 2011, Amazon.com announced a partnership with DC Comics for the exclusive digital rights to many popular comics, including Superman, Batman, Green Lantern, The Sandman, and Watchmen. The partnership has caused well-known bookstores like Barnes & Noble to remove these titles from their shelves.[33]

In November 2013, Amazon announced a partnership with the United States Postal Service to begin delivering orders on Sundays. The service, included in Amazon's standard shipping rates, initiated in metropolitan areas of Los Angeles and New York because of the high-volume and inability to deliver in a timely way, with plans to expand into Dallas, Houston, New Orleans and Phoenix by 2014.[34]

In June 2017, Nike confirmed a "pilot" partnership with Amazon to sell goods directly on the platform.[35][36][37]

As of October 11, 2017, AmazonFresh sold a range of Booths branded products for home delivery in selected areas.[38]

In September 2017, Amazon ventured with one of its sellers JV Appario Retail owned by Patni Group which has recorded a total income of US$ 104.44 million (₹ 759 crore) in financial year 2017–18.[39]

In November 2018, Amazon reached an agreement with Apple Inc. to sell selected products through the service, via the company and selected Apple Authorized Resellers. As a result of this partnership, only Apple Authorized Resellers may sell Apple products on Amazon effective January 4, 2019.[40][41]

Amazon.com's product lines available at its website include several media (books, DVDs, music CDs, videotapes and software), apparel, baby products, consumer electronics, beauty products, gourmet food, groceries, health and personal-care items, industrial & scientific supplies, kitchen items, jewelry, watches, lawn and garden items, musical instruments, sporting goods, tools, automotive items and toys & games.[citation needed] In August 2019, Amazon applied to have a liquor store in San Francisco, CA as a means to ship beer and alcohol within the city.[42] Amazon has separate retail websites for some countries and also offers international shipping of some of its products to certain other countries.[43]

Amazon.com has a number of products and services available, including:

AmazonFresh
Amazon Prime
Amazon Web Services
Alexa
Appstore
Amazon Drive
Echo
Kindle
Fire tablets
Fire TV
Video
Kindle Store
Music
Music Unlimited
Amazon Digital Game Store
Amazon Studios
AmazonWireless



"""

def get_entities(sent):
    ## chunk 1
    ent1 = ""
    ent2 = ""
    prv_tok_dep = ""  # dependency tag of previous token in the sentence
    prv_tok_text = ""  # previous token in the sentence
    prefix = ""
    modifier = ""
    #############################################################
    for tok in nlp(sent):
        ## chunk 2
        # if token is a punctuation mark then move on to the next token
        if tok.dep_ != "punct":
            # check: token is a compound word or not
            if tok.dep_ == "compound":
                prefix = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " " + tok.text
            # check: token is a modifier or not
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " " + tok.text
            ## chunk 3
            if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""
                ## chunk 4
            if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text
            ## chunk 5
            # update variables
            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text
    #############################################################
    return [ent1.strip(), ent2.strip()]

def get_relation(sent):
    # nlp = spacy.load('en_core_web_sm')
    doc = nlp(sent)
    # Matcher class object
    matcher = Matcher(nlp.vocab)
    #define the pattern
    pattern = [{'DEP':'ROOT'},
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},
            {'POS':'ADJ','OP':"?"}]
    matcher.add("matching_1", None, pattern)
    matches = matcher(doc)
    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]]
    return(span.text)


def process_text(text):
    bad_char = []
    for i in range(90):
        bad_char.append(str('[' + str(i) + ']'))
    for cha in bad_char:
        text = text.replace(cha,'')
    doc = nlp(text)

    sentences = [sent.string.strip() for sent in doc.sents]
    relations = [get_relation(i) for i in tqdm(sentences)]

    entity_pairs = []

    for i in tqdm(sentences):
        entity_pairs.append(get_entities(i))

    source = [i[0] for i in entity_pairs]
    target = [i[1] for i in entity_pairs]
    kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
    output = zip(source, relations, target)
    return(list(output))

print(process_text(text_amazon))
