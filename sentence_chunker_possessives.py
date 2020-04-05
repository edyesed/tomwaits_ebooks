#!/usr/bin/env python3
import nltk
import os
import pickle
import time
from collections import defaultdict

from neo4j import GraphDatabase

# uri = "bolt://localhost:7687"
uri = os.environ.get('NEO_URL', "bolt://neo:7687")
DEBUG = os.environ.get('DEBUG', False)

WORKING_DIR='./songs_pos_tagged_pickles'
## The pickles in INPUT_DIR are pickled whole song texts with tokenized words.
## INPUT_DIR has not been tokenized into sentences. 
INPUT_DIR='./pickled_lyrics'
#GRAMMAR = r"""
#  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
#      {<NNP>+}                # chunk sequences of proper nouns
#"""

#GRAMMAR = r"""
#  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
#  PP: {<IN><NP>}               # Chunk prepositions followed by NP
#  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
#  CLAUSE: {<NP><VP>}           # Chunk NP, VP
#"""

GRAMMAR = r"""
  NP: {<CD|DT|PP\$>?<JJ[RS]*|PRP\$*>*<NN.*>+} # Chunk sequences of DT, JJ, NN, chink out VPs
  PP: {<IN><NP>}                           # Chunk prepositions followed by NP
  VP: {<RB>?<VB[^RZ].*>+(<PRP><JJ>)*}             # Chunk verbs and their arguments
  INTERROGATION: {<VB.*><PRP><VB.*>}             # Ask a question
  INTERROGATIONLIKE: {<INTERROGATION><IN><PRP><.*>+?<NP>}   # Ask a question like a something
  VPastPart: {<VBN><IN>}                   # Chunk verbs and their arguments
  NOUNANDVERB: {<NP><VP>}                  # Chunk NP to VP
  VERBANDPREP: {<VP><PP>}
  """


def list_files(dir=""):
    files = [ f for f in os.listdir(dir) if 'pkl' in f ]
    return sorted(files)

def read_file(fname=None, dir=""):
    return nltk.data.load("/".join([dir, fname]), 'pickle')

def parse_sentence(sentence=None, grammar=None):
    pass

if __name__ == "__main__":
    for i in range(1,60):
        while True:
            try:
                driver = GraphDatabase.driver(uri, connection_timeout=120)
            except Exception as e:
                print(f"Error number {i}. {e}.")
                print(f"Error number {i} connecting to neo, sleeping for 2 seconds")
                time.sleep(2)
            break


    files = list_files(dir=INPUT_DIR)
    cp = nltk.RegexpParser(GRAMMAR)
    #stemmer = nltk.stem.SnowballStemmer('english')
    stemmer = nltk.stem.PorterStemmer()
    with driver.session() as session:
        for file in files:
            print(file)
            orig_filename = file.strip('.pkl')
            ## Songs already exist in neo courtesy of  graph_the_words.py

            pos_data = read_file(fname=file, dir=INPUT_DIR)
            for lyric in pos_data:
                #tokenized_sentence = nltk.tokenize.sent_tokenize(sentence)
                for lyric_idx, sentence in enumerate(lyric):
                    lyric_flat = ' '.join([w[0] for w in sentence])

                    chunks = cp.parse(sentence)
                    if DEBUG:
                        print(chunks.pprint())
                    care_about = ['VP', 'NP', 'VERBANDPREP', 'INTERROGATIONLIKE', 'INTERROGATION' ]
                    for chunk_idx, chunk in enumerate(chunks.subtrees(filter=lambda t: t.label() in care_about )):
                        if DEBUG:
                            print(chunk)
                            print("")
                        # We ensure that we send up the lyric once so we can relationship the lyric
                        #    to the phrase 
                        cypher = f"""
                                    MERGE (l:Lyric {{ text: "{lyric_flat}" }}) 
                                """

                        phrase = ' '.join([x[0] for x in chunk.flatten()]).lower()
                        cypher += f"""
                                 MERGE (pl{chunk_idx}:Phrase {{ text: "{phrase}" }})
                                 MERGE (pl{chunk_idx})<-[rl{chunk_idx}:{chunk.label()}]-(l)
                             """
                        try:
                            if DEBUG:
                                print(cypher)
                            session.run(cypher)
                        except Exception as e:
                            print(f"EXCEPTION RAISED phrase: {phrase}")
                            print(cypher)
                            print(e)

        # close out the neo session
        session.close()