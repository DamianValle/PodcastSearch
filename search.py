from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json

def search(es, index_name, search):
    res = es.search(index=index_name, body=search)
    return res

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

if __name__ == '__main__':
    es = connect_elasticsearch()
    if es is not None:
        search_object = {'query': { 
           "nested": {
                "path": "clips",
                "query": {
                    "nested": {
                        "path": "clips.words",
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                    "match_phrase": {
                                        "clips.words.word": "legitimacy"
                                    }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        },
                        "score_mode": "none"
                        }
                },
                "score_mode": "none"
                }
            }}
        res = search(es, 'podcasts', search_object)
        for hit in res['hits']['hits']:
            for h in hit["_source"]["clips"]:
                print(h["transcript"])