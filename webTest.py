import os,json
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
from GetIntervieweeInfo import ProcessInput,ExtractInfo

# UPLOAD_FOLDER = './uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/analyzeCV', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filepath = request.values.get('filepath')
        print('filepath is ', filepath)
        try:
            txt = ProcessInput(filepath)
            infoDict = ExtractInfo(txt)
            infoStr = json.dumps(infoDict, ensure_ascii=False, indent=4)
            return infoStr
        except Exception as e:
            errorDict = {}
            errorStr = json.dumps(errorDict, ensure_ascii=False, indent=4)
            return errorStr


        # return filepath
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         print('filename is :', filename)
    #         print('path : ',os.getcwd())
    #         print('save : ',os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #
    #         try:
    #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #             txt = ProcessInput(filepath)
    #             infoDict = ExtractInfo(txt)
    #             infoStr = json.dumps(infoDict, ensure_ascii=False, indent=4)
    #
    #             return infoStr
    #         except Exception as e:
    #             print('There is an error :',e)
    #
    #         # return redirect(url_for('uploaded_file',filename=filename))
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == "__main__":

    app.run(host='192.168.13.16',debug=True)
    app.run(debug=True)