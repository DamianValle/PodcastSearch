from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def print_all():
    i=1
    while True:
        try:
            res = es.get(index="bank", id=i)
        except:
            print("done")
            break
        print(res['_source'])
        print(i)
        
        i+=1

es = Elasticsearch()
s = Search(using=es)

#print_all()

res = es.search(index="bank", body={"query": {"match_all": {}}})

print(res)

print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(email)s %(city)s: %(age)s" % hit["_source"])
