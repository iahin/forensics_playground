from invoke import run
from pathlib import Path
import json
import yaml
import jsbeautifier
from tqdm import tqdm

rulespath = 'C:\\Users\\16sic\\Documents\\GitHub\\sladeworkplayground\\elasticsearch_sigma_module\\rules\\'
evtx_pattern = Path(rulespath).glob("**\*.yml")
evtx_file_list = [str(x) for x in evtx_pattern]

tempobj = []

for ymlfile in tqdm(evtx_file_list):
    try:
        arg = "sigmac -t es-qs -c C:\\Users\\16sic\\Documents\\GitHub\\sladeworkplayground\\elasticsearch_sigma_module\\config\\winglogbeat.yml " + \
            str(ymlfile)
        result = run(arg, hide=True, echo=False)
        result = result.stdout.strip()

        stream = open(ymlfile, 'r', encoding='utf-8')
        objlist = yaml.safe_load_all(stream)
        objlist = [x for x in objlist]

        for item in objlist:
            ttpidlist = []
            if 'tags' in item:
                if any(['attack.t' in x for x in item['tags']]):
                    ttpidlist = [''.join(x.split(".")[1:])
                                 for x in item['tags'] if 'attack.t' in x]
            for ttp in ttpidlist:
                tempobj.append({
                    "id": ttp,
                    "description": item['description'],
                    "query": result
                })
    except Exception as e:
        print(ymlfile)


writejson = open('./queries/querylist.json', 'w')
json.dump(tempobj, writejson)
