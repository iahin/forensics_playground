## Playbook

The current playbook module runs independently for demo purpose, to be integrated once confirmed in consensus. 

### Prerequisite

These are steps done to create the scripts

- Downloaded ElasticSearch
- Downloaded Sigma "windows" rules
- Downloaded Sigma config "helk.yml" for conversion
- Created a script to manually iterate through the windows rules folder to find all yml, gather all ttp id and queries associated to create a list of queries in JSON file
- Created a main.py script to call ES client, create index and upload preprocessed json log. Followed by loading the query and running a search

### To run the demo

1. Download Elasticsearch folder from the link above, extract and add the folder to "SLADE-KGA\CIE_server\playbook\", rename it to tools_elasticsearch
2. Run "SLADE-KGA\CIE_server\playbook\tools_elasticsearch\bin\elasticsearch.bat" to start the server
3. finally, run main.py to run a demo search on data in the data folder