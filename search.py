from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json
import pprint
from utils import find_time

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



def doSearch(word):
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
                                        "clips.words.word": search_word
                                    }
                                    }
                                ],
                                "minimum_should_match": 1
                            }
                        },
                        "score_mode": "avg"
                        }
                },
                "score_mode": "avg"
                }
            }}
        res = search(es, 'podcasts', search_object)
        result = [""]  # List of strings displayed in GUI
        for hit in res['hits']['hits']:
            for item in hit["_source"]["clips"]:
                if search_word in item["transcript"]:
                    find_time(search_word, item)
                result.append(item["transcript"])
        print(result)
        return result


if __name__ == '__main__':
    doSearch(search_word)
