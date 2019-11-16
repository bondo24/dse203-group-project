import os
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

def generate_wordcloud(output):
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
