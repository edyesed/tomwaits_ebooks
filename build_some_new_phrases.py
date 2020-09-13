#!/usr/bin/env python3
import os
import pickle
import time
import stanza
from collections import defaultdict

from neo4j import GraphDatabase


# uri = "bolt://localhost:7687"
uri = os.environ.get('NEO_URL', "bolt://neo:7687")
DEBUG = os.environ.get('DEBUG', False)

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

    with driver.session() as session:
        cypher = f"""
            MATCH (:Lyric)-[:VERBANDPREP]-(vp:Phrase)--(rw:RootWord) WHERE rw.text =~ $search 
            RETURN vp
        """
        res = session.run(cypher, search=".*dream.*")
        verbs = [x for x in res.values()]

        cypher = f"""
            MATCH (:Lyric)-[:NP]-(np:Phrase)--(rw:RootWord) WHERE rw.text =~ $search
            RETURN np
        """
        res = session.run(cypher, search="gun")
        nouns = [x for x in res.values()]
        for noun in nouns:
            print(noun[0]._properties['text'], len(noun[0]._graph._nodes.keys()))
            for verb in verbs:
                print(" ".join([noun[0]._properties['text'], verb[0]._properties['text']]))
