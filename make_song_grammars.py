#!/usr/bin/env python3
import nltk
import os
import pickle
import time
import pronouncing
import random
from collections import defaultdict
from pprint import pprint

from neo4j import GraphDatabase
#
# make a record of the POS tagged songs.
# Can we build a grammar from them? 
#

uri = os.environ.get('NEO_URL', "bolt://neo:7687")
DEBUG = os.environ.get('DEBUG', False)

WORKING_DIR='./songs_grammars'
## The pickles in INPUT_DIR are pickled whole song texts with tokenized words.
## INPUT_DIR has not been tokenized into sentences. 
INPUT_DIR='./pickled_lyrics'

def list_files(dir=""):
    files = [ f for f in os.listdir(dir) if 'pkl' in f ]
    return sorted(files)

def read_file(fname=None, dir=""):
    return nltk.data.load("/".join([dir, fname]), 'pickle')

def parse_sentence(sentence=None, grammar=None):
    pass


def find_a_rhyming_word(word=""):
    possible_replacements = pronouncing.rhymes(word)
    if len(possible_replacements) == 0:
        return word
    which_word = random.randint(0, len(possible_replacements) - 1)
    return possible_replacements[which_word]

def find_a_rhyming_phrase(lyric="", lyric_pos="", sub_parts_of_speech=[]):
    original_words = lyric.split()
    lyric_poses = lyric_pos.split()
    retphrase = ""
    sub_word_positions = list()
    for idx, x in enumerate(chorus_pos.split()):
        if x in sub_parts_of_speech:
            sub_word_positions.append(idx)
    #
    for idx, x in enumerate(lyric_poses):
        if idx in sub_word_positions:
            retphrase += find_a_rhyming_word(original_words[idx]) + " "
        else:
            retphrase += original_words[idx] + " "
    return  retphrase
 

    

if __name__ == "__main__":
    #for i in range(1,60):
    #    while True:
    #        try:
    #            driver = GraphDatabase.driver(uri, connection_timeout=120)
    #        except Exception as e:
    #            print(f"Error number {i}. {e}.")
    #            print(f"Error number {i} connecting to neo, sleeping for 2 seconds")
    #            time.sleep(2)
    #        break

    files = list_files(dir=INPUT_DIR)
    #stemmer = nltk.stem.SnowballStemmer('english')
    stemmer = nltk.stem.PorterStemmer()
    for file in files:
        print(file)
        orig_filename = file.strip('.pkl')
        ## Songs already exist in neo courtesy of  graph_the_words.py

        song_signature = defaultdict(int)
        song_sig_words = defaultdict(int)
        pos_data = read_file(fname=file, dir=INPUT_DIR)
        for lyric in pos_data:
            #tokenized_sentence = nltk.tokenize.sent_tokenize(sentence)
            for lyric_idx, sentence in enumerate(lyric):
                lyric_pos_flat = ' '.join([w[1] for w in sentence])
                lyric_words_flat = ' '.join([w[0] for w in sentence])
                #print(lyric_pos_flat)
                song_signature[lyric_pos_flat] += 1
                song_sig_words[lyric_pos_flat] = lyric_words_flat
                #except KeyError:
                #    song_signature[lyric_pos_flat] = 1
        ### Presumably, the repeating POS tags are the chorus
        chorus_pos = max(song_signature, key=song_signature.get)
        # exit fast if it's only one
        # otherwise, print the chorus
        if song_signature[chorus_pos] == 1:
            continue
        print("")
        suboutidxes = list()
        for idx, x in enumerate(chorus_pos.split()):
            if x in [ "VB", "VBG"]:
                suboutidxes.append(idx)
        
        original_words = song_sig_words[chorus_pos].split()
        print(chorus_pos)
        print(song_sig_words[chorus_pos])
        print(find_a_rhyming_phrase(lyric=song_sig_words[chorus_pos], 
                                    lyric_pos=chorus_pos, 
                                    sub_parts_of_speech=["VB", "VBG"]))

        #for idx, x in enumerate(chorus_pos.split()):
        #    if idx in suboutidxes:
        #        print(find_a_rhyming_word(original_words[idx]), "", end='')
        #    else:
        #        print(original_words[idx], "", end = '')
        print("")
        #for sig in sorted(song_signature, key=song_signature.get, reverse=True):
        #    print(sig, song_signature[sig])
        #pprint(dict(sorted(song_signature.items(), key=lambda item: item[1])))
        #pprint(song_signature)
