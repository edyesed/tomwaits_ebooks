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

from neo4j import GraphDatabase

uri = "bolt://neo:7687"
for i in range(1,60):
    while True:
        try:
            driver = GraphDatabase.driver(uri, auth=("neo4j", "bitnami"), connection_timeout=120)
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
            session.run(song_create)
            # sent is short for sentence
            # pos_tag_sents is seemingly a better way to pos_tag lists of sentences
            sent_toks = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(wordlist.raw(fid)))
            #for idx, sent in nltk.sent_tokenize(wordlist.raw(fid)):
            #    print(sent)
            #    print(sent_toks[idx])
            for idx, sent_parts in enumerate(sent_toks):
                sent = nltk.sent_tokenize(wordlist.raw(fid))[idx]
                print("""sent""")
                print(sent)
                sent_create = f"""MERGE (s:Lyric {{ text: $sent }}) return s"""
                print("""sent_create""")
                print(sent_create)
                try:
                    session.run(sent_create, sent=sent)
                except Exception as e:
                    print(e)
                sent_rel = f"""MATCH (s:Lyric),(n:Song) WHERE s.text=$sent AND n.title=$fid MERGE (n)-[r:PART_OF]-(s) RETURN type(r)"""
                print("""sent_rel""")
                print(sent_rel)
                try:
                    session.run(sent_rel, sent=sent, fid=fid)
                except Exception as e:
                    print(e)
                for word in sent_parts:
                    word_create = f"""MERGE (w:Word {{ text: $word, tag: $tag}}) """
                    print("""word_create""")
                    print(word_create)
                    try:
                        session.run(word_create, word=word[0], tag=word[1])
                    except Exception as e:
                        print(e)
                    word_rel = f"""MATCH (s:Lyric),(w:Word) WHERE s.text=$sent AND w.text=$text AND w.tag=$tag MERGE (w)-[r:PART_OF]-(s) RETURN type(r)"""
                    print("""word_rel""")
                    print(word_rel)
                    try:
                        session.run(word_rel, sent=sent, text=word[0], tag=word[1])
                    except Exception as e:
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