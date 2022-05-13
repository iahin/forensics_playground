import json

from kga.utils import tranformgraphfromjson, graphjson
from mongodb.MongoDBConnect import MongoDBConnect
from bson import ObjectId
from datetime import datetime, timedelta
from bson import json_util


class SladeDBAdaptor(MongoDBConnect):

    def __init__(self):
        super().__init__()

    def get_slade_caseobj(self, objid):
        try:
            collection = self.root["Cases"]
            objInstance = ObjectId(objid)
            collection = collection.find_one({"_id": objInstance})
            caseid = collection['CaseID']
            print('LOG: Successfully retrieved case object id from mongo.')
            return caseid
        except Exception as e:
            print('Exception | get_slade_caseobj() | ', e)
            return False

    def get_sladedetails(self, caseid):
        try:
            collection = self.root["Cases"]
            collection = collection.find_one(
                {"CaseID": caseid}, {'_id': False})
            print('LOG: Successfully retrieved case object from mongo.')
            return collection
        except Exception as e:
            print('Exception | get_sladedetails() | ', e)
            return False

    def get_caseidlist(self):
        try:
            collection = self.root["Cases"]
            collection = collection.distinct("CaseID")
            print('LOG: Successfully retrieved case object from mongo.')
            return collection
        except Exception as e:
            print('Exception | get_sladedetails() | ', e)
            return False

    def post_classification_result(self, caseid, machinelabel, score, userlabel, user):
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            collection = self.root["Intelligence"]
            datastore = {'classification': {"key": dt,
                                            "MacClassification": machinelabel,
                                            "Satfac": score,
                                            "UserCor": userlabel,
                                            "user": user}}
            collection.update_one(
                {'CaseID': caseid}, {'$push': datastore}, upsert=True)
            print('LOG: Successfully stored classification result to mongo.')
            return True
        except Exception as e:
            print('Exception | post_classification_result() | ', e)
            return False

    def get_classification_result(self, caseid):

        try:
            collection = self.root["Intelligence"]
            result = collection.find_one({'CaseID': caseid})
            result_obj = []
            if result:
                result_obj = result['classification']
            else:
                collection.update_one({'CaseID': caseid}, {
                    '$push': {'classification': []}}, upsert=True)
            print('LOG: Successfully retrieved classification result from mongo.')
            return result_obj
        except Exception as e:
            print('Exception | get_classification_result() | ', e)
            return False

    def close_case(self, caseid, fullname, reason):
        dt = datetime.now().isoformat()
        collection = self.root["Cases"]
        datastore = {
            "Status": "Closed", "CloseTime": dt, "CloseBy": fullname, "CloseReason": reason}
        collection.update_one({'CaseID': caseid}, {
            '$set': datastore}, upsert=True)

    def case2inteldb(self, caseid, crimetype, graphjsonobj):
        collection = self.root["Historical"]
        datastore = {"CrimeType": crimetype, "graph": graphjson(graphjsonobj)}
        collection.update_one({"CaseID": caseid}, {
            '$set': datastore}, upsert=True)

    def add_case_history(self, data):
        from datetime import datetime
        dt = datetime.now().isoformat()
        try:
            collection = self.root["Historical"]
            datastore = {"CloseTime": dt,
                         "CloseBy": data['fullname'],
                         "CloseReason": data['reason']}
            collection.update_one({'CaseID': data['objid']}, {
                '$set': datastore}, upsert=True)
            return True
        except Exception as e:
            print('Exception | close_case() | ', e)
            return False

    def gethistorical(self):
        # Get all historical graph data
        histcol = self.root['Historical']
        gethistorical = histcol.find({}, {'_id': False})
        historical = []
        for data in gethistorical:
            if 'Unauthorized Access' in data['CrimeType']:
                historical.append((tranformgraphfromjson(data['graph']), 0))
            if 'Data Theft' in data['CrimeType']:
                historical.append((tranformgraphfromjson(data['graph']), 1))
            if 'Unknown' in data['CrimeType']:
                historical.append((tranformgraphfromjson(data['graph']), 2))

        return historical

    def getcasegraph_nxobj(self, caseid):
        """
        return
        graphdata: networkx obj
        """
        intellicol = self.root['Intelligence']
        getintellicase = intellicol.find({'CaseID': caseid}, {'_id': False})
        graphjson = [x for x in getintellicase][0]['graph']
        getgraph = tranformgraphfromjson(graphjson)
        return getgraph

    def getgraphjson(self, caseid):
        """
        return
        graphdata: json obj
        """
        intellicol = self.root['Intelligence']
        getintellicase = intellicol.find({'CaseID': caseid}, {'_id': False})
        graphjson = [x for x in getintellicase][0]['graph']
        getgraph = tranformgraphfromjson(graphjson)
        return getgraph

    def getsimilarity(self, caseid):
        intellicol = self.root['Intelligence']
        historicol = intellicol.find_one(
            {'CaseID': caseid}, {'_id': False, "similarity": 1})
        result_obj = []

        if historicol:
            return historicol['similarity']
        else:
            return result_obj

    def gethistoricalwithcase(self):
        # to get caseid x graph
        histcol = self.root['Historical']
        gethistorical = histcol.find({}, {'_id': False})
        historical = []
        for data in gethistorical:
            historical.append(
                (data['CaseID'], tranformgraphfromjson(data['graph'])))

        return historical

    def getAllHistoricalCase(self):
        # to get caseid x graph
        histcol = self.root['Historical']
        gethistorical = histcol.find({}, {'_id': False})
        gethistorical = [x for x in gethistorical]
        return gethistorical

    def post_similarity_results(self, caseid, caseidlist):
        collection = self.root["Intelligence"]

        collection.update_one({'CaseID': caseid}, {
            '$set': {'similarity': caseidlist}}, upsert=True)

    def create_job(self, playbook, graphid, caseid, summary='test', ):
        from datetime import datetime
        dt = datetime.now().isoformat()
        try:
            Jobs = self.root["Jobs"]
            job = {"Playbook": playbook, "Summary": summary,
                   "GraphID": graphid, "CreatedDate": dt}

            x = Jobs.insert_one(job)

            cases = self.root["Cases"]
            objInstance = ObjectId(caseid)
            case = cases.find_one({"_id": objInstance})
            # jobsInsert=case["Jobs"]
            # case
            cases.update_one({'_id': objInstance},
                             {'$push': {'Jobs': str(x.inserted_id)}})
            return x.inserted_id
        except Exception as e:
            print('Exception | create_job() | ', e)
            return False

    def log_activity(self, userid, username, action, status):
        dt = datetime.now().isoformat()
        try:
            logs = self.root["ActivityLog"]
            log = {"LogTime": dt, "UserID": userid, "UserName": username, "Action": action, "Status": status}
            res = logs.insert_one(log)
            return res.inserted_id
        except Exception as e:
            print('Exception | log_activity() | ', e)
            return False

    def get_activities(self, user_id, start_time=datetime.now(), end_time=datetime.now()):
        log_collection = self.root["ActivityLog"]
        end_time = end_time + timedelta(days=1)
        return list(
            log_collection.find(
                {"UserID": user_id, "LogTime": {'$gte': start_time.isoformat(), '$lt': end_time.isoformat()}},
                {'_id': 0}
            )
        )
