
from climaterisks import transcript_collector

test = transcript_collector.get_earning_calls("Stoc_industries.xlsx")


import pandas as pd

from climaterisks import pre_processing 

report = pre_processing.get_ipcc_report("03_SROCC_Ch01_FINAL.txt")

list_reports = ["03_SROCC_Ch01_FINAL.txt",
                "04_SROCC_Ch02_FINAL.txt",
                "05_SROCC_Ch03_FINAL.txt",
                "06_SROCC_Ch04_FINAL.txt",
                "07_SROCC_Ch05_FINAL.txt",
                "08_SROCC_Ch06_FINAL.txt"]

reports, id2words, corpus = pre_processing.get_ipcc_reports(list_reports)



import gensim 



lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2words,
                                           num_topics=4, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=1,
                                           passes=50,
                                           alpha='auto')

print(lda_model.print_topics(10))
doc_lda = lda_model[corpus]

from gensim.models import CoherenceModel

coherence_model_lda = CoherenceModel(model=lda_model, texts=reports, dictionary=id2words, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()

