#!/usr/bin/env python
#
import nltk

def get_input_file(infile='./tests/ask_a_question.txt'):
    with open(infile) as inf:
        data = inf.readlines()
    return [x.strip() for x in data ]

def process_sentence_return_subject():
    pass


if __name__ == "__main__":
    intext = get_input_file()
    for sentence in intext:
        word_tags = nltk.word_tokenize(sentence)
        pos = nltk.pos_tag_sents([word_tags])[0]
        print(pos)
