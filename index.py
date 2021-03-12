from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es
  

def create_index(es, index_name='podcasts'):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "clips": {
                    "type": "nested",
                    "properties": {
                        "transcript": {"type": "text"},
                        "confidence": {"type": "double"},
                        "words": {
                            "type": "nested",
                            "properties": {
                                "startTime": {"type": "text"},
                                "endTime": {"type": "text"},
                                "word": {"type": "keyword"}
                            }
                        }
                    }
                },
            }
        }
    }
    try:
        if not es.indices.exists(index_name):
            print(es.indices.create(index=index_name, body=settings))
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def index_file(es, filename, index_name='podcasts'):
    with open(filename, 'r+') as f:
        res = {}
        data = json.load(f)
        res["title"] = filename
        clips = []
        for clip_data in data["results"]:
            clip_data = clip_data["alternatives"][0]
            if(not ("transcript" in clip_data.keys())):
                continue
            clip = {"transcript": clip_data["transcript"], "confidence": clip_data["confidence"], "words": clip_data["words"]}
            clips.append(clip)
            
        res["clips"] = clips

    print(es.index(index=index_name, body=res))


if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR)
  es = connect_elasticsearch()
  create_index(es)
  index_file(es, "sampleFile.json")
