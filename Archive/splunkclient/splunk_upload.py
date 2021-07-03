import json

import splunklib.client as client
import splunklib.results as results


def uploadLog(server_ip, username, password, indexname, logfile):
    try:
        session = client.connect(host=server_ip, port=8089,
                                 username=username, password=password, autologin=True)
    except Exception as e:
        return "Error"  # + str(e)
    else:
        myindex = session.indexes[indexname]
        # Submit an event over HTTP
        myindex.submit("This is my HTTP event", sourcetype=logfile,
                       host="local")


def createIndex(server_ip, username, password, indexname):
    try:
        session = client.connect(host=server_ip, port=8089,
                                 username=username, password=password, autologin=True)
    except Exception as e:
        return "Error"  # + str(e)
    else:
        if indexname in session.indexes:
            print("Index '%s' already exists" % indexname)
            return
        session.indexes.create(indexname)


HOST = 'localhost'
USER = 'admin'
PASS = 'admin123'
INDEXNAME = 'networklogs'
FILE='networklogs.csv'


createIndex(HOST, USER, PASS, INDEXNAME)
uploadLog(HOST, USER, PASS, INDEXNAME, FILE)
