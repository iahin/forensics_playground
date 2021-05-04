import pandas as pd
import json
from pprint import pprint

# df = pd.read_csv("winevent_datamodel.csv")
# df = df.drop(['Data Source', 'Sub - Data Source', 'Event ID', 'Description', 'Provider Name',
#               'Event Channel', 'Data Category', 'Data Sub-Category', 'Minimun Operating System', 'GPO', 'Enable Commands', 'Client Default', 'Server Default'], axis=1)

# df = df[["Data Object", "Relationship", "Data Object.1"]]
# print(df.head())

# df.to_csv('schema_1.csv', header=False)
# df = pd.read_csv("graph_schema.csv", header=None)

# print(df.head())

file = open("eventlogs.json")
jsonlist = json.load(file)

rel = set()

for dictitem in jsonlist:
    if any("target" in x for x in dictitem.keys()):
        # if ('eventid', '4656') in dictitem.items():

        rel.add(dictitem['eventid'])
        #print([x for x in dictitem.keys() if 'target' in x])
        #print([x for x in dictitem.keys() if 'registry' in x])

print(sorted(list(rel)))
