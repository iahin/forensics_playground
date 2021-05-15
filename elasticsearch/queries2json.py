from invoke import run
from pathlib import Path
import json
import yaml
import jsbeautifier
from tqdm import tqdm

rulespath = 'C:\\Users\\16sic\\Desktop\\elasticsearch\\rules\\'
evtx_pattern = Path(rulespath).glob("**\*.yml")
evtx_file_list = [str(x) for x in evtx_pattern]

tempobj = []

for item in tqdm(evtx_file_list):
    #schema = {"ttpname": [{"id":"", "description":"","name":"", "query":"" }],}

    try:
        arg = "sigmac -t es-dsl -c C:\\Users\\16sic\\Desktop\\elasticsearch\\config\\helk.yml " + \
            str(item)
        result = run(arg, hide=True, echo=False)
        objstr = result.stdout
        queryobj = json.loads(objstr)

        stream = open(item, 'r')
        obj = yaml.safe_load(stream)
        ttpidlist = [''.join(x.split(".")[1:])
                     for x in obj['tags'] if 'attack.t' in x]

        for ttp in ttpidlist:
            tempobj.append({
                "id": ttp,
                "description": obj['description'],
                "query": queryobj
            })
    except:
        print('error')


writejson = open('./queries/querylist.json', 'w')
json.dump(tempobj, writejson)
