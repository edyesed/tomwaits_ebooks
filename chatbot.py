#!/usr/bin/env python3
# coding: utf-8

# See https://github.com/parulnith/Building-a-Simple-Chatbot-in-Python-using-NLTK/blob/master/chatbot.py
# and https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e
#
#
# # Meet Robo: your friend

import nltk
import warnings
warnings.filterwarnings("ignore")

# nltk.download() # for downloading packages

import numpy as np
import random
import string # to process standard python strings


##f=open('allsongs.txt','r',errors = 'ignore')
##raw=f.read()
##raw=raw.lower()# converts to lowercase
corpus_root = './bin/download-lyrics'
wordlist = nltk.corpus.PlaintextCorpusReader(corpus_root, '.*txt')
raw = wordlist.raw()

#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
#nltk.download('tagsets') # tagsets, for getting help on upenn_tagset
#nltk.download('averaged_perceptron_tagger') # part-of-speech ( POS ) tagging
# FUN GAME, analyize a sentence.
# sent_tokens is the sentence-ized input
##  nltk.pos_tag(nltk.word_tokenize(sent_tokens[0]))
## >>> cb.sent_tokens[0]
## 'I plugged 16 shells from a thirty-ought-six\nand the Black Crow snuck through \na hole in the sky.'
## >>> cb.nltk.pos_tag(cb.nltk.word_tokenize(cb.sent_tokens[0]))
## [('I', 'PRP'), ('plugged', 'VBD'), ('16', 'CD'), ('shells', 'NNS'), ('from', 'IN'), ('a', 'DT'), ('thirty-ought-six', 'JJ'), ('and', 'CC'), ('the', 'DT'), ('Black', 'NNP'), ('Crow', 'NNP'), ('snuck', 'VBD'), ('through', 'IN'), ('a', 'DT'), ('hole', 'NN'), ('in', 'IN'), ('the', 'DT'), ('sky', 'NN'), ('.', '.')]
## >>> 

sent_detector = True 
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words
text_tokens = nltk.Text(word_tokens)

### Fun stuff

for x in range(0,10):
    print(f"SENT_TOKENS[{x}] ARE")
    print(sent_tokens[x])


#sent_tokens[:2]
#word_tokens[:5]


lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]



# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("TOM: If you want to exit, type Bye!")

if __name__ == "__main__":
    while(flag==True):
        user_response = input()
        user_response=user_response.lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                print("TOM: You are welcome..")
            else:
                if(greeting(user_response)!=None):
                    print("TOM: "+greeting(user_response))
                else:
                    print("TOM: ",end="")
                    print(response(user_response))
                    sent_tokens.remove(user_response)
        else:
            flag=False
            print("TOM: Bye! take care..")    