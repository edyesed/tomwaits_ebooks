#!/usr/bin/env python3
import nltk
import os
import pickle
import time
from collections import defaultdict

from neo4j import GraphDatabase

# uri = "bolt://localhost:7687"
uri = os.environ.get('NEO_URL', "bolt://neo:7687")

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
  NP: {<CD|DT|PP\$>?<JJ>*<NN.*>+} # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}                  # Chunk prepositions followed by NP
  VPastPart: {<VBN><IN>}          # Chunk verbs and their arguments
  VP: {<VB[^R].*>}                # Chunk verbs and their arguments
  NOUNANDVERB: {<NP><VP>}         # Chunk NP to VP
  VERBANDPREP: {<VP>+<PP>+}
  """

GEN_GRAMMAR = r"""
  
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
                # driver = GraphDatabase.driver(uri, auth=("neo4j", "bitnami"), connection_timeout=120)
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
            print(file)
            orig_filename = file.strip('.pkl')
            #song_create = f"""MERGE (s:Song {{ title: "{orig_filename}" }}) return s"""
            #try:
            #    session.run(song_create)
            #except Exception as e:
            #    print(f"EXCEPTION RAISED creating song {orig_filename}")
            #    print(e)

            pos_data = read_file(fname=file, dir=INPUT_DIR)
            #print(pos_data)
            for lyric in pos_data:
                #tokenized_sentence = nltk.tokenize.sent_tokenize(sentence)
                for sentence in lyric:
                    lyric_flat = ' '.join([w[0] for w in sentence])

                    print_s = False
                    chunks = cp.parse(sentence)
                    # care_about = ['NP', 'VP', 'PP', 'VPastPart', 'VERBANDPREP' ]
                    care_about = ['NP', 'VERBANDPREP', 'NOUNANDVERB']
                    for chunk in chunks.subtrees(filter=lambda t: t.label() in care_about ):
                    #for chunk in chunks.subtrees():
                        print("")
                        print("CHUNK")
                        print(chunk.label())
                        print(chunk)
                        phrase = ' '.join([x[0] for x in chunk.flatten()])
                        print(phrase)
                        #cypher = f"""
                        #            MERGE (l:Lyric {{ title: "{orig_filename}" }}) 
                        #        """
                        cypher = f"""
                                    MERGE (l:Lyric {{ text: "{lyric_flat}" }}) 
                                """
                        if chunk.label() == 'NP':
                            cypher += f"""
                                MERGE (p:Phrase {{ text: "{phrase}" }})
                                MERGE (p)<-[r:{chunk.label()}]-(l)
                            """
                        else:
                            counter = 0
                            for subt in chunk.subtrees():
                                phrase = ' '.join([x[0] for x in subt.flatten()])
                                cypher += f"""
                                    MERGE (p{counter}:Phrase {{ text: "{phrase}" }})
                                """
                                if counter == 0:
                                    cypher += f"""
                                    MERGE (p{counter})<-[r:{subt.label()}]-(s)
                                    """
                                if counter >0:
                                    cypher += f"""
                                    MERGE (p{counter})<-[r{counter}:{subt.label()}]-(p{counter-1})
                                    """
                                counter += 1

    
                    try:
                        session.run(cypher)
                    except Exception as e:
                        print(f"EXCEPTION RAISED phrase: {phrase}")
                        print(cypher)
                        print(e)

                    #try:
                    #    session.run(phrase_rel, song_title=orig_filename, phrase=phrase)
                    #except Exception as e:
                    #    print(f"EXCEPTION RAISED phrase_relationship: {phrase}")
                    #    print(e)

                    #if chunk.label() == 'NP' or chunk.label() == 'VP' \
                    #  or chunk.label() == 'PP' \
                    #  or chunk.label() == 'VPastPart':
                    #    print(f"""{chunk}""")
                    #    print_s = True
                    #if chunk.label()[0:2] == 'VP':
                    #    for bit in chunk:
                    #        print("STEM STEM")
                    #        print(stemmer.stem(bit[0]))
                if print_s:
                    print(sentence)
                #print(help(sentence))
        print("")