"""Pre processing, remove stopwords and lemmatization """

from matplotlib.cbook import report_memory
import nltk
nltk.download('stopwords')
import re
import numpy as np
import pandas as pd
from pprint import pprint
import spacy
from pandera.typing import DataFrame, DateTime, Object, Series
import pandera as pa
import gensim 
from nltk.corpus import stopwords
import gensim.corpora as corpora

def sent_to_words(sentences:list):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
    return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def make_bigrams(texts):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=100) # higher threshold fewer phrases.
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return [bigram_mod[doc] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    texts_out = [doc for doc in texts_out if len(doc) > 0]
    return texts_out

def get_ipcc(filePath:str):
    report = sum(pd.read_table(filePath).values.tolist(), [])
    report_words = list(sent_to_words(report))
    report_words = [word for word in report_words if len(word) > 0]
    report_words = remove_stopwords(report_words)
    report_words = make_bigrams(report_words)
    report_words = lemmatization(report_words)
    # Create Dictionary
    id2word = corpora.Dictionary(report_words)
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in report_words]
    return report_words, id2word, corpus

