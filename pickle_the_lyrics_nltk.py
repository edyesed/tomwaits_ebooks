#!/usr/bin/env python3
# coding: utf-8
#
# See https://github.com/parulnith/Building-a-Simple-Chatbot-in-Python-using-NLTK/blob/master/chatbot.py
# and https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e
#
# This file reads a set of plain text files ( i.e. song lyrics with punctuation )
#  and creates a neo4j database
# This file will drop words, tokens, and classifications into neo

import nltk
import warnings
import numpy as np
import random
import time
import string # to process standard python strings
import pickle
import os

from neo4j import GraphDatabase

uri = os.environ.get('NEO_URL', 'bolt://neo:7687')

for i in range(1,60):
    while True:
        try:
            # driver = GraphDatabase.driver(uri, auth=("neo4j", "bitnami"), connection_timeout=120)
            driver = GraphDatabase.driver(uri, connection_timeout=10)
        except Exception as e:
            print(f"Error number {i}. {e}.")
            print(f"Error number {i} connecting to neo, sleeping for 2 seconds")
            print(f"NEO_URL is {uri}")
            time.sleep(2)
        break

corpus_root = './bin/download-lyrics'
wordlist = nltk.corpus.PlaintextCorpusReader(corpus_root, '.*txt')



if __name__ == "__main__":
    with driver.session() as session:
        for fid in wordlist.fileids():
            print(fid)
            song_create = f"""MERGE (s:Song {{ title: "{fid}" }}) return s"""
            try:
                session.run(song_create)
            except Exception as e:
                print(f"EXCEPTION RAISED creating song {fid}")
                print(e)
            # sent is short for sentence
            # pos_tag_sents is seemingly a better way to pos_tag lists of sentences
            sentence_list = wordlist.raw(fid).split('\n\r\n')
            sent_toks = []
            for sentence in sentence_list:
                sent_toks.append(nltk.pos_tag_sents([nltk.word_tokenize(sentence)]))
            # Save that hard work into a pickle
            try:
                with open(f'pickled_lyrics/{fid}.pkl', "wb") as out_f:
                    pickle.dump(sent_toks, out_f)
            except Exception as e:
                print("Exception raised while pickling")
                print(e)
            # Try and stash the indivicual words.
            #  this seems... hmm.. idk
            ##for idx, sent in enumerate(sent_toks):
            ##    lyric = ""
            ##    for subsent in sent:
            ##        lyric += ' '.join([word for word,POS in subsent])
            ##    sent_create = f"""MERGE (l{idx}:Lyric {{ text: $text }}) return l{idx}"""
            ##    print(f"""sent_create : {sent_create}""")
            ##    print(f"""sent_create text:{lyric}""")
            ##    try:
            ##        session.run(sent_create, text=lyric)
            ##    except Exception as e:
            ##        print("EXCEPTION RAISED create sent_create")
            ##        print(e)
            ##    sent_rel = f"""MATCH (s:Lyric),(n:Song) WHERE s.text=$sent AND n.title=$fid MERGE (n)-[r:SONG_LYRIC]-(s) RETURN type(r)"""
            ##    try:
            ##        session.run(sent_rel, sent=lyric, fid=fid)
            ##    except Exception as e:
            ##        print("EXCEPTION RAISED sent_rel")
            ##        print(e)

### ED NOTES
# see https://www.nltk.org/book/ch05.html
#>>> f = open('pickled_lyrics/big_joe_and_phantom_309.txt.pkl', 'rb')
#>>> obj = pickle.load(f)
#>>> f.close()
#>>> obj
# pos is word with counts
# i.e. 
# >>> for k in pos.keys():
# ...    print(k, len(pos[k]))
# ... 
# See 1
# , 54
# I 32
# >>> pos = nltk.Index(wor for sent in obj for wor in sent)
# pos2 is words by tag_pos
# i.e. 
# 
# >>> pos2['NN']
# ['coast', 'buck', 'everybody', 'luck', 'way', 'hometown', 'couple', 'week', 'luck', 'way', 'night', 'rain', 'man', 'chill', 'time', 'time', 'semi', 'hill', 'air', 'cab', 'wheel', 'wheel', 'man', 'hand', 'grin', 'name', 'rig', 'rig',
#>>> pos2 = nltk.Index((wor[1],wor[0]) for sent in obj for wor in sent)
# MOST COMMON WORD