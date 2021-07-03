from datetime import datetime
from elasticsearch import Elasticsearch
import json
from numpy import fabs
import pandas as pd
from pprint import pprint
from elasticsearch_dsl import Search

# sigmac -t 'es-dsl' -c .\helk.yml .\win_alert_active_directory_user_control.yml

es = Elasticsearch()
index_name = 'spf2'


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
    searchContext = Search(using=es, index=index_name)
    s = searchContext.query('query_string', query=queryobj)
    response = s.execute()

    if response.success():
        result = [d.to_dict() for d in s.scan()]
        if result:
            return result


# es.indices.delete(index=index_name)
# loglist = loadlog('data\methods_cache_evtx.json')
# uploader(loglist)


queryobj = loadqueries('.\\queries\querylist.json')
for item in queryobj:
    querystring = item['query']
    if searcher(querystring):
        print(item['id'])
