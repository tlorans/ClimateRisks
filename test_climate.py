
from climaterisks import transcript_collector

test = transcript_collector.get_earning_calls("Stoc_industries.xlsx")


import pandas as pd

from climaterisks import pre_processing 

reports, id2words, corpus = pre_processing.get_ipcc("03_SROCC_Ch01_FINAL.txt")

[[(id2words[id], freq) for id, freq in cp] for cp in corpus[:1]]


import gensim 

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2words,
                                           num_topics=7, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

print(lda_model.print_topics())

from gensim.models import CoherenceModel

coherence_model_lda = CoherenceModel(model=lda_model, texts=reports, dictionary=id2words, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
