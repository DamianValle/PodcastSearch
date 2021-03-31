from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json
import pprint
from utils import *

search_word = "you"

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
        search_object = { "from" : 0,
        "size" : 50,
        # 'explain': True,
        'query': { 
           "nested": {
                "path": "clips",
                "query": {
                    "bool": {
                        "should": [
                            {
                            "match_phrase": {
                                "clips.transcript": search_word
                            }
                            }
                        ],
                        "minimum_should_match": 1
                    }
                },
                "score_mode": "avg"
                }
            }}
##        search_object = {'query': {'match': {'show_description': 'this'} }
##            }
##        res = search(es, 'metadata', search_object)
##        for hit in res['hits']['hits']:
##            print(hit["_source"]["show_uri"])
##            print(hit["_source"]["show_name"])
##            print(hit["_source"]["show_description"])

        
        res = search(es, 'podcasts', search_object)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(res["explanation"])
        for hit in res['hits']['hits']:
            #print(hit["_source"]["title"])
            #print("uri: ", parse_filename2uri(hit["_source"]["title"]))

            meta_search_object = {
                'query': {'match': {'show_uri': parse_filename2uri(hit["_source"]["title"])}}
                }

            metadata = search(es, 'metadata', meta_search_object)

            for h in metadata['hits']['hits']:
                print(h["_source"]["show_description"])
            
            print(hit["_score"])
            # for item in hit["_source"]["clips"]:
            #     if search_word in item["transcript"]:
            #         find_time(search_word, item)
