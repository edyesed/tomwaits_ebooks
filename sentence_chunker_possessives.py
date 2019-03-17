#!/usr/bin/env python3
import nltk
import os
import pickle
from collections import defaultdict

DIR='./songs_pos_tagged_pickles'
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
  PP: {<IN><NP>}               # Chunk prepositions followed by NP
  VPastPart: {<VBN><IN>}      # Chunk verbs and their arguments
  VP: {<VB.*>}           # Chunk verbs and their arguments
  CLAUSE: {<PRP|DT|IN>}      # Chunk NP, VP
  """

GEN_GRAMMAR = r"""
  
  """

def list_files(dir=DIR):
    files = [ f for f in os.listdir(dir) if 'pkl' in f ]
    return sorted(files)

def read_file(fname=None, dir=DIR):
    return nltk.data.load("/".join([DIR, fname]), 'pickle')

def parse_sentence(sentence=None, grammar=None):
    pass

if __name__ == "__main__":
    files = list_files()
    cp = nltk.RegexpParser(GRAMMAR)
    for file in files:
        print(file)
        print(file)
        pos_data = read_file(fname=file)
        #print(pos_data)
        for sentence in pos_data:
            print_s = False
            chunks = cp.parse(sentence)
            for chunk in chunks.subtrees():
                #print(chunk)
                if chunk.label() == 'NP' or chunk.label() == 'VP' \
                  or chunk.label() == 'PP' \
                  or chunk.label() == 'VPastPart':
                    print(f"""{chunk}""")
                    print_s = True
                if chunk.label()[0:2] == 'VP':
                    for bit in chunk:
                        
                    print("WHAT WHAT")
            if print_s:
                print(sentence)
            #print(help(sentence))
        print("")