import pandas as pd
import stanfordnlp
stanfordnlp.download('en')

nlp = stanfordnlp.Pipeline()

# text_e = output["competitors"]['Netflix']['summary'].strip('\n').lower()
def stanford_pos(output):
    # text_netflix = "netflix inc (/ˈnɛtflɪks/) is an american media-services provider and production company headquartered in los gatos california founded in 1997 by reed hastings and marc randolph in scotts valley california the company's primary business is its subscription-based streaming service which offers online streaming of a library of films and television programs including those produced in-house9 as of april 2019 netflix had over 148 million paid subscriptions worldwide including 60\xa0million in the united states and over 154\xa0million subscriptions total including free trials8 it is available worldwide except in mainland china (due to local restrictions) syria north korea and crimea (due to us sanctions) the company also has offices in the netherlands brazil india japan and south korea10 netflix is a member of the motion picture association (mpa)"

    # dictionary that contains pos tags and their explanations
    pos_dict = {'CC': 'coordinating conjunction', 'CD': 'cardinal digit', 'DT': 'determiner',
                'EX': 'existential there (like: \"there is\" ... think of it like \"there exists\")',
                'FW': 'foreign word', 'IN': 'preposition/subordinating conjunction', 'JJ': 'adjective \'big\'',
                'JJR': 'adjective, comparative \'bigger\'', 'JJS': 'adjective, superlative \'biggest\'',
                'LS': 'list marker 1)', 'MD': 'modal could, will', 'NN': 'noun, singular \'desk\'',
                'NNS': 'noun plural \'desks\'', 'NNP': 'proper noun, singular \'Harrison\'',
                'NNPS': 'proper noun, plural \'Americans\'', 'PDT': 'predeterminer \'all the kids\'',
                'POS': 'possessive ending parent\'s', 'PRP': 'personal pronoun I, he, she',
                'PRP$': 'possessive pronoun my, his, hers', 'RB': 'adverb very, silently,',
                'RBR': 'adverb, comparative better', 'RBS': 'adverb, superlative best',
                'RP': 'particle give up', 'TO': 'to go \'to\' the store.', 'UH': 'interjection errrrrrrrm',
                'VB': 'verb, base form take', 'VBD': 'verb, past tense took',
                'VBG': 'verb, gerund/present participle taking', 'VBN': 'verb, past participle taken',
                'VBP': 'verb, sing. present, non-3d take', 'VBZ': 'verb, 3rd person sing. present takes',
                'WDT': 'wh-determiner which', 'WP': 'wh-pronoun who, what', 'WP$': 'possessive wh-pronoun whose',
                'WRB': 'wh-abverb where, when', 'QF': 'quantifier, bahut, thoda, kam (Hindi)', 'VM': 'main verb',
                'PSP': 'postposition, common in indian langs', 'DEM': 'demonstrative, common in indian langs'
                }

    # extract parts of speech
    def extract_pos(doc):
        parsed_text = {'word': [], 'pos': [], 'exp': []}
        for sent in doc.sentences:
            for wrd in sent.words:
                if wrd.pos in pos_dict.keys():
                    pos_exp = pos_dict[wrd.pos]
                else:
                    pos_exp = 'NA'
                parsed_text['word'].append(wrd.text)
                parsed_text['pos'].append(wrd.pos)
                parsed_text['exp'].append(pos_exp)
        # return a dataframe of pos and text
        return pd.DataFrame(parsed_text)

    NN_df = []
    j = 'acquisitions'
    if j == 'acquisitions':
        for i in output[j]:
            text_e = output[j][i]['summary'].strip('\n').lower()
            doc = nlp(text_e)
            #extract pos
            pos_df = extract_pos(doc)

            NN_df[i] = pos_df[pos_df['pos'] == 'NN']
            for row in NN_df[i]['word']:
                NN_df[i] = NN_df[i][NN_df[i]['word'] != str(i).lower()]
                NN_df[i] = NN_df[i][NN_df[i]['word'] !=  'amazon']
                if row in output['acquisitions']['Woot']['founder'].lower().split():
                    NN_df[i] = NN_df[i][NN_df[i]['word'] != row]

    print(NN_df)


    # print(pos_df[pos_df['pos'] == 'NN'])
