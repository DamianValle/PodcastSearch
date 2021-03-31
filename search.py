from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json
import pprint
from utils import *
import pprint

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
        search_object = { "from" : 0,
        "size" : 10,
        # 'explain': True,
        'query': { 
           "nested": {
                "path": "clips",
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
                },
                "score_mode": "avg"
                }
            }}

        res = search(es, 'podcasts', search_object)

        for hit in res['hits']['hits']:

            elem = {}

            #print(hit["_source"]["title"])
            #print("uri: ", parse_filename2uri(hit["_source"]["title"]))

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

        for hit in res['hits']['hits']:
            pprint.pprint(hit["_score"])
            
        result = [""]  # List of strings displayed in left side of GUI
        extraInfo = [""]  # Extra info in right side of GUI
        for hit in res['hits']['hits']:
            for item in hit["_source"]["clips"]:
                if search_word in item["transcript"]:
                    find_time(search_word, item)
            print(hit["metadata"])
            result.append(" " + hit["metadata"]["_source"]["show_name"] + ", " + hit["metadata"]["_source"]["episode_name"])
            extraInfo.append(hit["metadata"]["_source"]["episode_description"])
        print(result)
        return [result,extraInfo]
            

if __name__ == '__main__':
    doSearch(search_word)
