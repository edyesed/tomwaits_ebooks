#!/usr/bin/env python 
import nltk
import os
import time

import nltk

from neo4j import GraphDatabase

# uri = "bolt://localhost:7687"
uri = os.environ.get('NEO_URL', "bolt://neo:7687")
DEBUG = os.environ.get('DEBUG', False)

GRAMMAR = r"""
  NP: {<CD|DT|PP\$>?<JJ[RS]*|PRP\$*>*<NN.*>+} # Chunk sequences of DT, JJ, NN, chink out VPs
  PP: {<IN><PR.*>*<N.*>}                           # Chunk prepositions followed by NP
  XPP: {<IN><.*>+<N.*>}                           # Chunk prepositions followed by NP
  VP: {<VB(?!P).*>+<RB>*(<PRP><JJ>)*}             # Chunk verbs and their arguments
  NOUNANDVERB: {<NP><VP>}                  # Chunk NP to VP
  VERBANDPREP: {<VP><PP>}
  GOODNOUNSANDVERBS: {<NN.*><VB.*>+}
  SENTENCE: {<NOUNANDVERB><PP>}
  """

def connect_to_neo(uri=""):
    for i in range(1,60):
        while True:
            try:
                driver = GraphDatabase.driver(uri, connection_timeout=120)
            except Exception as e:
                print(f"Error number {i}. {e}.")
                print(f"Error number {i} connecting to neo, sleeping for 2 seconds")
                time.sleep(2)
            break
    return driver

def get_random_phrases(session=None, p_type="" ):
    rwords = list()
    cypher = f"""MATCH NounBit=(p:Phrase)-[r:{p_type}]-() RETURN p.text, rand() as x order by x LIMIT 10"""
    words = session.run(cypher)
    for w in words:
        rwords.append(w['p.text'])
    return rwords


def filter_good_sentences(noun_phrases=[], verb_phrases=[]):
    sentences = list()
    rD = dict()
    for noun in noun_phrases:
        for verb in verb_phrases:
            sentence = " ".join([noun, verb])
            sentences.append(sentence)
    for sentence in sentences:
        tokenized = nltk.word_tokenize(sentence)
        postagged = nltk.pos_tag(tokenized)
        chunks = cp.parse(postagged)
        care_about = ['SENTENCE' ]
        for chunk_idx, chunk in enumerate(chunks.subtrees(filter=lambda t: t.label() in care_about )):
            rD[sentence] = {"chunks": chunks, "pos": postagged}
    return rD
    

if __name__ == "__main__":
    cp = nltk.RegexpParser(GRAMMAR)
    stemmer = nltk.stem.PorterStemmer()
    driver = connect_to_neo(uri=uri)

    noun_phrases = list()
    verb_phrases = list()

    with driver.session() as session:
        noun_phrases = get_random_phrases(session=session, p_type="NP")
        verb_phrases = get_random_phrases(session=session, p_type="VERBANDPREP")

    prototype_phrases = list()
    keep_sentences = dict()
    
    keep_sentences = filter_good_sentences(noun_phrases=noun_phrases, verb_phrases=verb_phrases)
    
    if DEBUG:
        for sentence, bits in keep_sentences.items():
            print(sentence)
            for idx, tree in enumerate(bits['chunks'].subtrees()):
                print(tree)
            print(bits['pos'])

    for sentence in keep_sentences.keys():
        print(sentence)
        

        


