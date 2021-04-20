from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json
import pprint
from utils import *
import pprint
from results import Results

search_word = "porn"

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

def doSearch(word, score_mode,k=10,interval_size=1):

    result = {}

    es = connect_elasticsearch()
    if es is not None:
        search_object = { "from" : 0,
        "size" : k,
        # 'explain': True,
        'query': {
           "nested": {
                "path": "clips",
                "query": {
                    "function_score": {
                        "field_value_factor": {
                            "field": "confidence",
                            "factor": 1.0,
                            "modifier": "none",
                            "missing": 1
                        },
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                    "match_phrase": {
                                        "clips.transcript": word
                                    }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        }
                    }
                },
                "inner_hits": {},
                "score_mode": score_mode
                }
            }}

        res = search(es, 'podcasts', search_object)

        for hit in res['hits']['hits']:

            show_uri, episode_uri = parse_filename2uri(hit["_source"]["title"])

            meta_search_object = {
                "query": {
                    "bool": {
                    "must": [
                        {
                        "match": {
                            "show_uri": show_uri
                        }
                        },
                        {
                        "match": {
                            "episode_uri": episode_uri
                        }
                        }
                    ]
                    }
                }
            }

            metadata = search(es, 'metadata', meta_search_object)

            hit["metadata"] = metadata['hits']['hits'][0]

        return Results.createFromSearch(res, search_word=word, interval_size=interval_size)
            

if __name__ == '__main__':
    doSearch(search_word, score_mode='avg')
