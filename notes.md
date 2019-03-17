# Notes for myself

# ED NOTES
(https://www.nltk.org/book/ch05.html)[https://www.nltk.org/book/ch05.html]

oad pickled files
ython
open('pickled_lyrics/big_joe_and_phantom_309.txt.pkl', 'rb')
= pickle.load(f)
ose()
obj
s = [wor[0] for sent in obj for wor in sent]
```

Words counted by frequency
g nltk to do word counts, and counts by pos_tag

ython
TICE THIS SNEAKY ASS LIST COMPREHENSION
= nltk.Index(wor for sent in obj for wor in sent)
k in pos.keys():
print(k, len(pos[k]))
e 1
54
32
```


ython
ME SNEAKY LIST COMPREHENSION
 = nltk.Index((wor[1],wor[0]) for sent in obj for wor in sent)
s2['NN']
coast', 'buck', 'everybody', 'luck', 'way', 'hometown', 'couple', 'week', 'luck', 'way', 'night', 'rain', 'man', 'chill', 'time', 'time', 'semi', 'hill', 'air', 'cab', 'wheel', 'wheel', 'man', 'hand', 'grin', 'name', 'rig', 'rig',
```

YPHER Notes
 finds the words and counts them by their frequency in all lyrics

```
H (n:Word)-[r:LYRIC_WORD]-() RETURN n.tag, n.text, count(r) ORDER BY count(r) DESC
```

Edu stuff
ttps://www.lexalytics.com/lexablog/text-analytics-functions-explained
hunking in the NLTK book https://www.nltk.org/book/ch07.html
 Generator https://github.com/thallada/nlp/blob/master/syntax_aware_generate.py
his is what linked to the Generator https://www.hallada.net/2017/07/11/generating-random-poems-with-python.html
arts of Speech for POS tagging : https://medium.com/@gianpaul.r/tokenization-and-parts-of-speech-pos-tagging-in-pythons-nltk-library-2d30f70af13b

|| Label  | Description || 
|-----|----| 
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
