import requests
from requests.auth import HTTPBasicAuth

API = 'http://li2190-224.members.linode.com/'
username = 'sladeadmin'
password = 'sit-custodio-slade-8787'


def caseListAll():
    try:
        ENDPOINT = 'case/list'
        URL = API + ENDPOINT
        print("Getting case details, please wait...")
        response = requests.get(URL, auth=HTTPBasicAuth(username, password))
        print(response.json())
    except Exception as e:
        print(e)


def listallttp():
    ENDPOINT = 'case/enrich/ttps'
    URL = API + ENDPOINT
    response = requests.get(URL, auth=HTTPBasicAuth(username, password))
    if response:
        print('Success!')
        print('Result: ', str(response.json()))
    else:
        print('An error has occurred | ', str(response.json()))


caseListAll()
listallttp()