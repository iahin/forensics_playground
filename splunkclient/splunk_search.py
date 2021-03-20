import csv
import json
from pprint import pprint

import splunklib.client as client
import splunklib.results as results


def fetch_results(server_ip, username, password, search_qry, time_range):
    try:
        session = client.connect(host=server_ip, port=8089,
                                 username=username, password=password, autologin=True)
    except Exception as e:
        return "Error"  # + str(e)
    else:
        kwargs_export = {#"earliest_time": "-%sh" % time_range,"latest_time": "now",
                         "search_mode": "normal"}
        exportsearch_results = session.jobs.export("search " + search_qry, **kwargs_export)

        # Get the results using the ResultsReader and convert to json serialzable data
        reader = results.ResultsReader(exportsearch_results)
        search_result = filter(lambda result: isinstance(result, dict), reader)
        search_result = {"data": list(search_result)}
        session.logout()
        return search_result

HOST = 'localhost'
QUERY = 'index=windowsevent Source_Address=* Destination_Address=*  | fields Source_Address Destination_Address' #extract source and dest IP
USER = 'admin'
PASS = 'admin123'
TIMERANGE = 0

result = fetch_results(HOST, USER, PASS, QUERY, TIMERANGE)
with open('data.json', 'w') as f:
    json.dump(result, f)