from datetime import datetime
from elasticsearch import Elasticsearch
import logging, json
import os
import csv


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
            "number_of_replicas": 0,
            "index": {"mapping" : {"nested_objects": {"limit": 50000}}},
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

def create_and_index_metadata(es, index_name='metadata'):
    settings = {
        "settings": {"number_of_shards": 1,
            "number_of_replicas": 0
            },
        "mappings": {
            "properties": {
                "uri": {"type": "text"},
                "title": {"type": "text"},
                "description": {"type": "text"}
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

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = '..\podcasts-no-audio-13GB\spotify-podcasts-2020-summarization-testset\metadata-summarization-testset.tsv'
    print(os.path.join(fileDir, filename))

    with open(os.path.join(fileDir, filename), 'r+', encoding="utf8") as f:
        read_tsv = csv.reader(f, delimiter = "\t")
        headers = next(read_tsv, None)

        print(headers)
        for row in read_tsv:
            res = {}
            res["show_uri"] = row[0]
            res["show_name"] = row[1]
            res["show_description"] = row[2]

            print(es.index(index=index_name, body=res))
    

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

    # es.indices.delete(index='metadata', ignore=[400, 404])
    create_index(es)

    index_metadata = False
    if index_metadata:
        create_and_index_metadata(es)

    for subdir, dirs, files in os.walk(r'../podcasts-no-audio-13GB/spotify-podcasts-2020-summarization-testset'):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".tsv"):
                print (filepath)
                #metadata
            if filepath.endswith(".json"):
                #actual data
                print (filepath)
                index_file(es, filepath)

    #index_file(es, "sampleFile.json")
