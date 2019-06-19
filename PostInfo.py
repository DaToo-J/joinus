import os,json
import logging,sys
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
from GetIntervieweeInfo import ProcessInput,ExtractInfo

app = Flask(__name__)
@app.route('/analyzeCV', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        filepath = request.values.get('filepath')
        try:
            txt = ProcessInput(filepath)
            infoDict = ExtractInfo(txt)
            infoStr = json.dumps(infoDict, ensure_ascii=False, indent=4)
            return infoStr
        except Exception as e:
            errorDict = {}
            errorStr = json.dumps(errorDict, ensure_ascii=False, indent=4)
            return errorStr

    elif request.method == 'GET':
        return 'haha'

if __name__ == "__main__":
    app.run(host='192.168.13.169',debug=False, threaded=True)