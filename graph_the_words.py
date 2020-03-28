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

from neo4j import GraphDatabase

uri = "bolt://neo:7687"
for i in range(1,60):
    while True:
        try:
            # driver = GraphDatabase.driver(uri, auth=("neo4j", "bitnami"), connection_timeout=120)
            driver = GraphDatabase.driver(uri, connection_timeout=120)
        except Exception as e:
            print(f"Error number {i}. {e}.")
            print(f"Error number {i} connecting to neo, sleeping for 2 seconds")
            time.sleep(2)
        break

class HelloWorldExample(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


##f=open('allsongs.txt','r',errors = 'ignore')
##raw=f.read()
##raw=raw.lower()# converts to lowercase
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
            sent_toks = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(wordlist.raw(fid).split('\n')))
            try:
                with open(f'pickled_lyrics/{fid}.pkl', "wb") as out_f:
                    pickle.dump(sent_toks, out_f)
            except Exception as e:
                print("Exception raised while pickling")
                print(e)
            #for idx, sent in nltk.sent_tokenize(wordlist.raw(fid)):
            #    print(sent)
            #    print(sent_toks[idx])
            for idx, sent_parts in enumerate(sent_toks):
                sent = nltk.sent_tokenize(wordlist.raw(fid))[idx]
                print("""sent""")
                print(sent)
                sent_create = f"""MERGE (s:Lyric {{ text: $text }}) return s"""
                print(f"""sent_create text:{sent}""")
                try:
                    session.run(sent_create, text=sent)
                except Exception as e:
                    print("EXCEPTION RAISED create sent_create")
                    print(e)
                sent_rel = f"""MATCH (s:Lyric),(n:Song) WHERE s.text=$sent AND n.title=$fid MERGE (n)-[r:SONG_LYRIC]-(s) RETURN type(r)"""
                print(f"""sent_rel sent:{sent} fid:{fid}""")
                try:
                    session.run(sent_rel, sent=sent, fid=fid)
                except Exception as e:
                    print("EXCEPTION RAISED sent_rel")
                    print(e)
                for word,tag in sent_parts:
                    word_create = f"""MERGE (w:Word {{ text: $word, tag: $tag}}) """
                    print(f"""word_create text:{word} tag:{tag}""")
                    try:
                        # Always drop the individual words in lower case
                        #session.run(word_create, word=word[0].lower(), tag=word[1])
                        session.run(word_create, word=word.lower(), tag=tag)
                    except Exception as e:
                        print("EXCEPTION RAISED word_create")
                        print(e)
                    word_rel = f"""MATCH (s:Lyric),(w:Word) WHERE s.text=$sent AND w.text=$word AND w.tag=$tag MERGE (w)-[r:LYRIC_WORD]-(s) RETURN type(r)"""
                    print(f"""word_rel sent:{sent} word:{word} tag:{tag}""")
                    try:
                        session.run(word_rel, sent=sent, word=word.lower(), tag=tag)
                    except Exception as e:
                        print("EXCEPTION RAISED word_rel")
                        print(e)
                #print(nltk.sent_tokenize(wordlist.raw(fid))[idx])
            print(" stop spot ")
            print(" stop spot ")
            print(" stop spot ")
            #for sent in nltk.sent_tokenize(wordlist.raw(fid)):
            #    print(nltk.pos_ta
            #    print(sent)
            #raw = wordlist.words(fid).raw()
            #word_tokens = wordlist.words(fid)
            #sent_detector = True 
            #sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
            #word_tokens = nltk.word_tokenize(raw)# converts to list of words
            #text_tokens = nltk.Text(word_tokens)
            #for token in sent_tokens:
            #    print(nltk.pos_tag(nltk.word_tokenize(token)))


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