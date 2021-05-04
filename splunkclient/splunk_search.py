import csv
import json
from pprint import pprint

import splunklib.client as client
import splunklib.results as results

import pandas as pd
import re
from tqdm import tqdm


def fetch_results(server_ip, username, password, search_qry, time_range):

    try:
        session = client.connect(host=server_ip, port=8089,
                                 username=username, password=password, autologin=True)
    except Exception as e:
        return "Error"  # + str(e)
    else:
        kwargs_export = {  # "earliest_time": "-%sh" % time_range,"latest_time": "now",
            "search_mode": "normal"}

        exportsearch_results = session.jobs.export(
            "search " + search_qry, **kwargs_export)
        # Get the results using the ResultsReader and convert to json serialzable data
        reader = results.ResultsReader(exportsearch_results)
        search_result = filter(
            lambda result: isinstance(result, dict), reader)
        search_result = {"data": list(search_result)}
        session.logout()

        return search_result


HOST = 'localhost'
# extract source and dest IP
#QUERY = 'source="eventlogs.json" index="test1" sourcetype="_json" LogonType=*'
USER = 'admin'
PASS = 'admin123'
TIMERANGE = 0

# result = fetch_results(HOST, USER, PASS, QUERY, TIMERANGE)
# with open('data.json', 'w') as f:
#     json.dump(result, f)

# Load query list from lookup into datafram
df = pd.read_csv("lookup\splunk_scrapped.csv")

# Get only the rows with "windows security" as providing technology category
s = df['providing_technologies']
df = df[s.str.contains('Windows Security', case=False)]
df_query = df['qualified_search'].tolist()


def changeField(patterntype, inputstring, string2change):
    regex = re.compile(patterntype)
    newstring = re.sub(regex, string2change, inputstring)
    print(newstring)

    return newstring


newquery = []
index_pattern = r"index=(\S+)"
index2change = "index=test1"

source_pattern = r"source=(\S+)"
source2change = "source=eventlogs.json"

sourcetype_pattern = r"sourcetype=(\S+)"
sourcetype2change = "sourcetype=_json"

eventcode_pattern = r"EventCode"
eventcode2change = "EventID"

lookup_pattern = r"Logon_Type"
lookup2change = "LogonType"

user_pattern = r"user"
user2change = "User"

for item in df_query:

    if isinstance(item, str) and item:
        index_stringproc = changeField(index_pattern, item, index2change)
        source_stringproc = changeField(
            source_pattern, index_stringproc, source2change)
        sourcetype_stringproc = changeField(
            sourcetype_pattern, source_stringproc, sourcetype2change)
        eventcode_stringproc = changeField(
            eventcode_pattern, sourcetype_stringproc, eventcode2change)

        lookup_stringproc = eventcode_stringproc.replace(
            lookup_pattern, lookup2change)

        user_stringproc = lookup_stringproc.replace(user_pattern, user2change)

        newquery.append(user_stringproc)

with open('data.json', 'w') as f:
    json.dump({"data": newquery}, f)

count = []

for item in tqdm(newquery):
    try:
        result = fetch_results(HOST, USER, PASS, item, TIMERANGE)
        if any(result["data"]):
            print(result)
            count.append(result)
    except:
        pass


print(len(count))
