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

