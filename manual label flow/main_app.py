"""
Main SLADE API with cyvestigo graph construction module. !!! Not in use for now.
"""
import json
import os
import posixpath
from pathlib import Path

import requests
from flask import request, jsonify, Flask
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

from cyvestigo.CyvestigoMain import CyvestigoMainClass
from kga.main import get_similairty_graph, newdatapredict, relable, run_similarcase
from lipe.LipeMain import LipeMain
from mongodb.SladeDBAdaptor import SladeDBAdaptor
from playbook import playbook_flow_genv5 as playbook_flow_gen
from datetime import datetime

UPLOAD_FOLDER = casepath = str(Path.joinpath(
    Path(__file__).resolve().parents[1], 'casedata'))

CASEPATH = str(Path.joinpath(Path(__file__).resolve().parents[1], 'casedata'))

app = Flask(__name__)
CORS(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 70000 * 1024 * 1024


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'img', 'dd'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return "<h1> HELLO WORLD </>"


@app.route('/create_case', methods=['POST'])
def create_case():
    objid = request.args.get('objid')

    sladedbadaptor = SladeDBAdaptor()
    caseid = sladedbadaptor.get_slade_caseobj(objid)

    cyvestigocaller = CyvestigoMainClass(CASEPATH, caseid)
    cyvestigocaller.create_case(objid)

    preproc = LipeMain(CASEPATH, caseid)
    result = preproc.create_folders()

    if result:
        resp = jsonify({'message': result})
        resp.status_code = 200
    else:
        resp = jsonify({'message': 'Folders already created.'})
        resp.status_code = 400
    return resp


@app.route('/close_case', methods=['POST'])
def close_case():
    request_data = request.get_json()
    sladedbadaptor = SladeDBAdaptor()
    sladedbadaptor.close_case(request_data['CaseID'], request_data['fullname'], request_data['reason'])
    graphjsonobj = sladedbadaptor.getgraphjson(request_data['CaseID'])
    sladedbadaptor.case2inteldb(request_data['CaseID'], request_data['LastClassificCrimeType'], graphjsonobj)

    resp = jsonify({'message': 'Case has closed'})
    resp.status_code = 200

    return resp


@app.route('/store_image', methods=['POST'])
def store_image():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    caseid = request.args.get('caseid')
    files = request.files.getlist('file')
    preproc = LipeMain(CASEPATH, caseid)

    for file in files:
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp

        if not allowed_file(file.filename):
            resp = jsonify(
                {'message': 'Allowed file types are .img and .dd'})
            resp.status_code = 400
            return resp

        imagepath = Path(preproc.diskimage, file.filename)
        if imagepath.is_file():
            resp = jsonify(
                {'message': 'Disk image already uploaded'})
            resp.status_code = 400
            return resp

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(
            app.config['UPLOAD_FOLDER'], caseid, 'image', filename)))
    resp = jsonify({'message': 'File successfully uploaded.'})
    resp.status_code = 201
    return resp


@app.route('/hash_image', methods=['POST'])
def hash_image(caseid, imagename):
    # caseid = request.args.get('caseid')
    try:
        preproc = LipeMain(CASEPATH, caseid)
        preproc.hash_img(imagename)
        resp = jsonify({'message': 'Evidence hashed in database.'})
        resp.status_code = 201
        return resp
    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/extract_artifacts', methods=['POST'])
def extract_artifacts(caseid, imagename):
    # caseid = request.args.get('caseid')
    # imagename = request.args.get('filename')
    drive, path = os.path.splitdrive(CASEPATH)
    imagepath = '/mnt/' + drive.lower().replace(':', '') + str(os.path.join(path, caseid, 'image')).replace(os.sep,
                                                                                                            posixpath.sep)
    cachepath = '/mnt/' + drive.lower().replace(':', '') + str(os.path.join(path, caseid, 'cache')).replace(os.sep,
                                                                                                            posixpath.sep)
    extractedpath = '/mnt/' + drive.lower().replace(':', '') + str(os.path.join(path, caseid, 'extracted')).replace(
        os.sep,
        posixpath.sep)

    PARAMS = {'imagepath': imagepath,
              'cachepath': cachepath,
              'extractedpath': extractedpath,
              'imagename': imagename}

    try:
        resp = requests.post(
            'http://localhost:8000/ingest-image', params=PARAMS)
        assert resp
        resp = jsonify({'message': 'Artifacts extracted.'})
        resp.status_code = 201
        return resp
    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/preprocess_artifacts', methods=['POST'])
def preprocess_artifacts(caseid):
    caseid = request.args.get('caseid')
    preproc = LipeMain(CASEPATH, caseid)
    preproc.parse_logs()
    try:
        resp = jsonify({'message': 'Evidence preprocessed.'})
        resp.status_code = 201
        return resp
    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/submit_evidence', methods=['POST'])
def submit_evidence():
    caseid = request.args.get('caseid')
    filenamelist = request.get_json()['filenamelist']
    for filename in filenamelist:
        hash_image(caseid, filename)
        extract_artifacts(caseid, filename)
        preprocess_artifacts(caseid)
        cyvestigocaller = CyvestigoMainClass(CASEPATH, caseid)
        cyvestigocaller.upload_artifacts()
    try:
        resp = jsonify({'message': 'Evidence preprocessed.'})
        resp.status_code = 201
        return resp
    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/search_ttp', methods=['GET'])
def search_ttp():
    caseid = request.args.get('caseid')
    ttpid = request.args.get('ttpid')
    cyvestigocaller = CyvestigoMainClass(CASEPATH, caseid)
    try:
        ttpesult = cyvestigocaller.search_ttp(ttpid)

        if ttpesult['nodes']:
            resp = jsonify({'ttp_exist': 'true'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'ttp_exist': 'false'})
            resp.status_code = 400
            return resp

    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/search_anyttps', methods=['GET'])
def search_anyttps():
    caseid = request.args.get('caseid')
    cyvestigocaller = CyvestigoMainClass(CASEPATH, caseid)
    try:
        ttps = cyvestigocaller.search_any_ttp()
        if ttps:
            resp = jsonify({'ttps': ttps})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'ttps': None})
            resp.status_code = 400
            return resp

    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/get_caseidlist', methods=['GET'])
def get_caseidlist():
    sladedbadaptor = SladeDBAdaptor()
    result = sladedbadaptor.get_caseidlist()

    if result:
        resp = jsonify({'message': result})
        resp.status_code = 200
    else:
        resp = jsonify({'message': 'Server error.'})
        resp.status_code = 400
    return resp


@app.route('/get_casedetails', methods=['GET'])
def get_casedetails():
    caseid = request.args.get('caseid')
    sladedbadaptor = SladeDBAdaptor()
    result = sladedbadaptor.get_sladedetails(caseid)

    if result:
        resp = jsonify({'message': result})
        resp.status_code = 200
    else:
        resp = jsonify({'message': 'Server error.'})
        resp.status_code = 400
    return resp


@app.route('/get_classification_result', methods=['GET'])
def get_classification_result():
    caseid = request.args.get('caseid')
    sladedbadaptor = SladeDBAdaptor()
    result = sladedbadaptor.get_classification_result(caseid)
    resp = jsonify({'message': result})
    resp.status_code = 200
    # if result:
    #     resp = jsonify({'message': result})
    #     resp.status_code = 200
    # else:
    #     resp = jsonify({'message': 'Server error.'})
    #     resp.status_code = 400
    return resp


@app.route('/run_prediction', methods=['GET'])
def run_prediction():
    # First prediction
    caseid = request.args.get('caseid')
    sladedbadaptor = SladeDBAdaptor()
    histdata = sladedbadaptor.gethistorical()
    newdata = sladedbadaptor.getcasegraph_nxobj(caseid)

    pred, proba = newdatapredict(histdata, newdata)
    label = ""
    score = ""
    if pred == 0:
        label = "Unauthorized Access"
        score = str(proba) + '%'
    if pred == 1:
        label = "Data Theft"
        score = str(proba) + '%'
    if pred == 2:
        label = "Unknown"
        score = str(proba) + '%'

    userlabel = ''
    user = ''
    machinelabel = label
    score = score
    result = sladedbadaptor.post_classification_result(
        caseid, machinelabel, score, userlabel, user)

    if result:
        resp = jsonify({'message': result})
        resp.status_code = 200
    else:
        resp = jsonify({'message': 'Server error.'})
        resp.status_code = 400
    return resp


@app.route('/post_classification_result', methods=['POST'])
def reclassify():
    # Relabel and retrain
    caseid = request.args.get('caseid')
    userlabel = request.get_json()['userlabel']
    user = request.get_json()['user']

    labelparse = 0
    if "Unauthorized Access" in userlabel:
        labelparse = 0
    if "Data Theft" in userlabel:
        labelparse = 1
    if "Unknown" in userlabel:
        labelparse = 2

    # Get data from intel db
    sladedbadaptor = SladeDBAdaptor()
    histdata = sladedbadaptor.gethistorical()
    newdata = sladedbadaptor.getcasegraph_nxobj(caseid)

    # Feed to ML model to learn new
    relable(histdata, newdata, labelparse)

    # get prediction from retrained model
    pred, proba = newdatapredict(histdata, newdata)

    label = ""
    score = ""
    if pred == 0:
        label = "Unauthorized Access"
        score = str(proba) + '%'
    if pred == 1:
        label = "Data Theft"
        score = str(proba) + '%'
    if pred == 2:
        label = "Unknown"
        score = str(proba) + '%'

    result = sladedbadaptor.post_classification_result(
        caseid, label, score, userlabel, user)

    if result:
        resp = jsonify({'message': result})
        resp.status_code = 200
    else:
        resp = jsonify({'message': 'Server error.'})
        resp.status_code = 400
    return resp


@app.route('/get_histsimilarity', methods=['GET'])
def get_histsimilarity():
    caseid = request.args.get('caseid')
    sladedbadaptor = SladeDBAdaptor()
    simdata = sladedbadaptor.getsimilarity(caseid)
    resp = jsonify({'message': simdata})
    return resp


@app.route('/get_allhistricalcase', methods=['GET'])
def get_allhistricalcase():
    sladedbadaptor = SladeDBAdaptor()
    simdata = sladedbadaptor.getAllHistoricalCase()
    resp = jsonify({'message': simdata})
    return resp


@app.route('/run_histsimilarity', methods=['POST'])
def run_histsimilarity():
    caseid = request.args.get('caseid')
    sladedbadaptor = SladeDBAdaptor()
    histcasegraphdata = sladedbadaptor.gethistoricalwithcase()
    currentcasegraph = sladedbadaptor.getcasegraph_nxobj(caseid)
    simcaseidlist = run_similarcase(currentcasegraph, histcasegraphdata)
    sladedbadaptor.post_similarity_results(caseid, simcaseidlist)

    resp = jsonify({'message': "DONE"})
    return resp


@app.route('/get_similarity_graph', methods=['POST'])
def get_similarity_graph():
    caseid = request.args.get('caseid')
    pair2caseid = request.get_json()['pair2caseid']

    print(caseid, pair2caseid)

    sladedbadaptor = SladeDBAdaptor()

    pair1graph = sladedbadaptor.getcasegraph_nxobj(caseid)
    pair2graph = sladedbadaptor.getcasegraph_nxobj(pair2caseid)

    simcaseidlist = get_similairty_graph(pair1graph, pair2graph)

    print(simcaseidlist)

    resp = jsonify({'message': simcaseidlist})
    return resp


@app.route('/gen_playbook', methods=['GET'])
def gen_playbook():
    ttpid = request.args.get('ttpid')

    try:
        flowlist = playbook_flow_gen.generateFlowWrapper(ttpid)
        print(flowlist)

        if flowlist:
            resp = jsonify({'playbook': flowlist})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'playbook': None})
            resp.status_code = 400
            return resp

    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/execute_playbook', methods=['GET'])
def execute_playbook():
    ttpid = request.args.get('ttpid')
    cyobjid = request.args.get('cyobjid')
    playbook = request.args.get('playbook')
    caseid = request.args.get('caseid')
    ttplist = playbook_flow_gen.genPlaybookTtps(ttpid)
    print(ttplist.extend(['T1086', 'T1059']))
    try:
        cyvestigocaller = CyvestigoMainClass(CASEPATH, cyobjid)
        ttpgraph = cyvestigocaller.searchMulTtps(cyobjid, ttplist)

        if ttpgraph:
            resp = jsonify({'ttpgraph': ttpgraph})
            resp.status_code = 200

        else:
            resp = jsonify({'ttpgraph': None})
            resp.status_code = 400
        sladedbadaptor = SladeDBAdaptor()
        result = sladedbadaptor.create_job(playbook, 'sub_graph', caseid)

        return resp

    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/get_ttps', methods=['GET'])
def get_ttps():
    tactic = request.args.get('tactic')
    ttps = playbook_flow_gen.get_ttps(tactic)
    if ttps:
        resp = jsonify({'ttps': ttps})
        resp.status_code = 200
    else:
        resp = jsonify({'ttps': 'fail to load ttps'})
        resp.status_code = 400
    return resp


@app.route('/crimetype_playbook', methods=['GET'])
def crimetype_playbook():
    tactic = request.args.get('tactic')
    ttps = playbook_flow_gen.generateRedPlaybook(tactic)
    caseid = request.args.get('cyobjid')
    cyvestigocaller = CyvestigoMainClass(CASEPATH, caseid)
    try:
        ttpresult = cyvestigocaller.search_any_ttp().keys()
        if ttpresult:
            set1 = set(ttps)
            set2 = set(ttpresult) | {'T1055', 'T1078'}
            print(set1, set2)
            iset = set1.intersection(set2)
            res = list(iset)

            resp = jsonify({'ttps': res})
            resp.status_code = 200
        else:
            resp = jsonify({'ttps': 'fail to load ttps'})
            resp.status_code = 400
        return resp

    except Exception as e:
        print(e)
        resp = jsonify({'message': 'There was error in the process.'})
        resp.status_code = 400
        return resp


@app.route('/get_activities', methods=['POST'])
def get_activities():
    request_data = request.get_json()
    userid = request_data['userid']
    startdate = request_data['startdate']
    enddate = request_data['enddate']
    sladedbadaptor = SladeDBAdaptor()
    result = sladedbadaptor.get_activities(
        userid,
        datetime.strptime(startdate, '%Y-%m-%d'),
        datetime.strptime(enddate, '%Y-%m-%d')
    )

    resp = jsonify({'message': result})
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3004, debug=True, use_reloader=False)

# use this args on cli to run
# set FLASK_APP = temp_app.py
# flask run
