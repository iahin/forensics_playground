from datetime import datetime
from elasticsearch import Elasticsearch
import json
import pandas as pd
from pprint import pprint

# sigmac -t 'es-dsl' -c .\helk.yml .\win_alert_active_directory_user_control.yml

es = Elasticsearch()
index_name = 'sladeindex'


def loadlog(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data


def loadqueries(queryfile):
    with open(queryfile) as f:
        data = json.loads(f.read())
    return data


def uploader(jsonlist):
    for item in jsonlist:
        es.index(index=index_name, body=item)


def searcher(queryobj):
    searchresult = []
    searchContext = es.search(
        index=index_name,
        body=queryobj)

    totalhits = searchContext['hits']['total']['value']
    for doc in searchContext['hits']['hits']:
        searchresult.append(doc['_source'])

    return totalhits, searchresult


# es.indices.delete(index=index_name)
# loglist = loadlog('data\evtx_artifacts.json')
# uploader(loglist)

queryobj = loadqueries('.\\queries\querylist.json')

# sample ttp to search 1055,1547
for item in queryobj:
    if '1110' in item['id']:
        querystring = item['query']
        hits, searchstring = searcher(querystring)
        if hits > 0:
            print("TTP detected: ", item['id'])
            print("Index in log: ", searchstring)
