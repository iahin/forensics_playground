

from email.mime import image
import json
import os
import posixpath
from pathlib import Path
import requests

from lipe.LipeMain import LipeMain
from lipe.utils_evtxlog import evtxextract, evtxpreprocess, payloadpreprocess
from lipe.utils_ntfslog import getSystemName, ntfslog_ext, proc_csv2dictlist, proc_samtxt, proc_systemtxt
from glob import glob

CASEPATH = 'B:\\custodio_gen_img'
CASEPATHLIST = glob(CASEPATH+'/*')


#caseimageslist = [os.path.join(path, name) for path, subdirs, files in os.walk(CASEPATH) for name in files]

for caseimg in CASEPATHLIST:
    #drive, path = os.path.splitdrive(caseimg)

    #p = Path(caseimg)
    # imagename = str(Path(*p.parts[-1:]))
    # imagepath = Path(*p.parts[:-1])
    # print(imagepath)

    # posiximgpath = '/mnt/' + drive.lower().replace(':', '') + str(imagepath).replace(os.sep, posixpath.sep)
    # cachepath = '/mnt/' + drive.lower().replace(':', '') + str(os.path.join(imagepath, 'cache')).replace(os.sep,
    #                                                                                                         posixpath.sep)
    # extractedpath = '/mnt/' + drive.lower().replace(':', '') + str(os.path.join(imagepath, 'extracted')).replace(
    #     os.sep,
    #     posixpath.sep)

    # PARAMS = {'imagepath': posiximgpath,
    #           'cachepath': cachepath,
    #           'extractedpath': extractedpath,
    #           'imagename': imagename}

    # try:
    #     resp = requests.post('http://localhost:8000/ingest-image', params=PARAMS)
    #     assert resp
    #     print("Extracted image; ", imagename)

    # except Exception as e:
    #     print("Something went wrong for image"+ imagename + " : " + str(e))

    imagepath = caseimg
    cachepath = str(Path(imagepath, 'cache'))
    parseevtx =  str(Path(cachepath , "parsed_evtx.json"))
    extractedpath = str(Path(imagepath , 'extracted'))
    outputpath = str(Path(imagepath , 'output', "combined_artifacts.json"))

    try: 
        dictlist = evtxextract(extractedpath)
        dictlist = evtxpreprocess(dictlist)
        dictlist = payloadpreprocess(dictlist)
        json.dump(dictlist, open(parseevtx, 'w'))

        ntfslog_ext(extractedpath, cachepath)

        EVTX = json.load(open(parseevtx))
        SAM = proc_samtxt(cachepath)
        SYSTEM = proc_systemtxt(cachepath)
        SDS = proc_csv2dictlist(cachepath, "SDS")
        MFT = proc_csv2dictlist(cachepath, "MFT")
        J = proc_csv2dictlist(cachepath, "J")
        EvidenceMarking = getSystemName(cachepath)

        # artifacts_obj = {
        #     'EvidenceMarking': EvidenceMarking,
        #     'MFT': MFT,
        #     'J': J,
        #     'SDS': SDS,
        #     'SAM': [SAM],
        #     'SYSTEM': [SYSTEM],
        #     'EVTX': EVTX,
        #     'properties': {}
        # }
        artifacts_obj = {
            'EvidenceMarking': EvidenceMarking,
            'MFT': [],
            'J': [],
            'SDS': [],
            'SAM': [],
            'SYSTEM': [],
            'EVTX': EVTX,
            'properties': {}
        }
        json.dump(artifacts_obj,  open(outputpath, 'w'))
    
    except Exception as e:
        print("!!!!!!!!!!!!!!! Something went wrong for image"+ imagepath + " : " + str(e))