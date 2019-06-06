import os,json
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
from GetIntervieweeInfo import ProcessInput,ExtractInfo

app = Flask(__name__)
@app.route('/analyzeCV', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filepath = request.values.get('filepath')
        # print('filepath is ', filepath)
        try:
            txt = ProcessInput(filepath)
            infoDict = ExtractInfo(txt)
            infoStr = json.dumps(infoDict, ensure_ascii=False, indent=4)
            return infoStr
        except Exception as e:
            errorDict = {}
            errorStr = json.dumps(errorDict, ensure_ascii=False, indent=4)
            return errorStr

if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
    app.run(debug=True)