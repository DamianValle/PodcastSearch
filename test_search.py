from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json
import os


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es
  

def search(es, index_name='podcasts'):
    res = es.search(index=index_name, body=
                    {'query': {
                        'match': {
                            'title': '8'
                            }
                        }
                     })
    
    print(res['hits']['hits'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    es = connect_elasticsearch()
    search(es)


