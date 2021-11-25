from datetime import datetime
from elasticsearch import Elasticsearch
import json
from elasticsearch.client import eql
from numpy import fabs
import pandas as pd
from pprint import pprint
from elasticsearch_dsl import Search

es = Elasticsearch(http_auth=('sitslade', 'admin123'))
index_name = 'cfred'

querystring = "process where process.executable in (\"start\", \"process_started\") and\n  process.executable: (\"powershell.exe\", \"pwsh.exe\") and process.executable : \"New-MailboxExportRequest*\""
objfsdd = {
    "query": querystring
}
csada = eql.EqlClient(es)
searching = csada.search(index=index_name, body=objfsdd)
print(searching)
