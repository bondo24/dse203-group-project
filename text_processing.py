import spacy
import textacy
nlp = spacy.load('en')

def subject_verb_object_triples(text):
    text = nlp(text)
    return textacy.extract.subject_verb_object_triples(text)
