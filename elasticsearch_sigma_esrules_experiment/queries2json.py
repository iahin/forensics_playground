from invoke import run
from pathlib import Path
import json
import yaml
import jsbeautifier
from tqdm import tqdm
import toml
from pprint import pprint

rulespath = 'C:\\Users\\16sic\\Desktop\\esc base rules\\windows\\'
evtx_pattern = Path(rulespath).glob("**\*.toml")
evtx_file_list = [str(x) for x in evtx_pattern]

tempobj = []


for tomlfile in tqdm(evtx_file_list[:1]):
    toml_obj = toml.loads(open(tomlfile).read(), _dict=dict)
    description = toml_obj['rule']['description']
    description = description.strip()
    ttpid = toml_obj['rule']['threat'][0]['technique'][0]['id']
    ttpid = ttpid.lower()
    query = toml_obj['rule']['query']
    query = query.strip()

    tempobj.append({
        "id": ttpid,
        "description": description,
        "query": query
    })


writejson = open('./queries/querylist.json', 'w')
json.dump(tempobj, writejson)
