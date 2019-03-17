# Notes for myself

# ED NOTES
see (https://www.nltk.org/book/ch05.html)[https://www.nltk.org/book/ch05.html]

## Load pickled files
```python
f = open('pickled_lyrics/big_joe_and_phantom_309.txt.pkl', 'rb')
obj = pickle.load(f)
f.close()
obj
words = [wor[0] for sent in obj for wor in sent]
```

##  Words counted by frequency
Using nltk to do word counts, and counts by pos_tag

```python
# NOTICE THIS SNEAKY ASS LIST COMPREHENSION
pos = nltk.Index(wor for sent in obj for wor in sent)
for k in pos.keys():
    print(k, len(pos[k]))
# See 1
# , 54
# I 32
```


```python
# SAME SNEAKY LIST COMPREHENSION
pos2 = nltk.Index((wor[1],wor[0]) for sent in obj for wor in sent)
# pos2['NN']
# ['coast', 'buck', 'everybody', 'luck', 'way', 'hometown', 'couple', 'week', 'luck', 'way', 'night', 'rain', 'man', 'chill', 'time', 'time', 'semi', 'hill', 'air', 'cab', 'wheel', 'wheel', 'man', 'hand', 'grin', 'name', 'rig', 'rig',
```

## CYPHER Notes
This finds the words and counts them by their frequency in all lyrics

```
MATCH (n:Word)-[r:LYRIC_WORD]-() RETURN n.tag, n.text, count(r) ORDER BY count(r) DESC
```

##  Edu stuff
1. https://www.lexalytics.com/lexablog/text-analytics-functions-explained
2. Chunking in the NLTK book https://www.nltk.org/book/ch07.html
3. A Generator https://github.com/thallada/nlp/blob/master/syntax_aware_generate.py
4. This is what linked to the Generator https://www.hallada.net/2017/07/11/generating-random-poems-with-python.html
5. Parts of Speech for POS tagging : https://medium.com/@gianpaul.r/tokenization-and-parts-of-speech-pos-tagging-in-pythons-nltk-library-2d30f70af13b

    || Label  | Description || 
    | CC | coordinating conjunction |
    | CD | cardinal digit |
    | DT | determiner |
    | EX | existential there (like: “there is” … think of it like “there exists”) |
    | FW | foreign word |
    | IN | preposition/subordinating conjunction |
    | JJ | adjective ‘big’ |
    | JJR | adjective, comparative ‘bigger’ |
    | JJS | adjective, superlative ‘biggest’ |
    | LS | list marker 1) |
    | MD | modal could, will |
    | NN | noun, singular ‘desk’ |
    | NNS | noun plural ‘desks’ |
    | NNP | proper noun, singular ‘Harrison’ |
    | NNPS | proper noun, plural ‘Americans’ |
    | PDT | predeterminer ‘all the kids’ |
    | POS | possessive ending parent’s |
    | PRP | personal pronoun I, he, she |
    | PRP$ | possessive pronoun my, his, hers |
    | RB | adverb very, silently, |
    | RBR | adverb, comparative better |
    | RBS | adverb, superlative best |
    | RP | particle give up |
    | TO, | to go ‘to’ the store. |
    | UH | interjection, errrrrrrrm |
    | VB | verb, base form take |
    | VBD | verb, past tense took |
    | VBG | verb, gerund/present participle taking |
    | VBN | verb, past participle taken |
    | VBP | verb, sing. present, non-3d take |
    | VBZ | verb, 3rd person sing. present takes |
    | WDT | wh-determiner which |
    | WP | wh-pronoun who, what |
    | WP$ | possessive wh-pronoun whose |
    | WRB | wh-abverb where, when |
