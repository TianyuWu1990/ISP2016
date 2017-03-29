import glob
import os

import shutil
import xml
from codecs import ignore_errors, open

import time

import re

import sys


import WebCaseHandler
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file

# Initialize the Flask application
from werkzeug.utils import secure_filename

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


# remove directory function
def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, os.stat.S_IWRITE)
    os.unlink(path)


# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['DOWNLOAD_FOLDER'] = 'WebPostProcessing/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_txt'] = set(['txt'])
app.config['ALLOWED_json'] = set(['json'])


# For a given file, return whether it's an allowed type or not
def allowed_txt(filename):
    return '.' in filename and \
           filename.split('.', 1)[1] in app.config['ALLOWED_txt']


def allowed_json(filename):
    return '.' in filename and \
           filename.split('.', 1)[1] in app.config['ALLOWED_json']


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('FDA_Textmining.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    # # Clear uploads for the new uploading
    cwd_uploads = os.getcwd() + '/uploads'
    files = glob.glob(cwd_uploads)
    for f in files:
        shutil.rmtree(f, onerror=on_rm_error)
    if not os.path.exists(cwd_uploads):
        os.makedirs(cwd_uploads)

    open("HTML_info/RawName.txt", 'w').close()
    open("HTML_info/age.txt", 'w').close()
    open("HTML_info/drug.txt", 'w').close()
    open("HTML_info/eventdate.txt", 'w').close()
    open("HTML_info/gender.txt", 'w').close()
    open("HTML_info/weight.txt", 'w').close()

    # Get the name of the uploaded file_Raw
    file_Raw = request.files['file_Raw']
    file_Con = request.files['file_Con']
    # Check if the file_Raw is one of the allowed types/extensions
    if file_Raw and file_Con and allowed_txt(file_Raw.filename) and allowed_json(file_Con.filename):
        # Make the filename_raw safe, remove unsupported chars
        filename_raw = secure_filename(file_Raw.filename)
        f = open('HTML_info/RawName.txt', 'w')
        f.write(filename_raw)  # python will convert \n to os.linesep
        f.close()
        # Move the file_Raw form the temporal folder to
        # the upload folder we setup
        file_Raw.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_raw))
        # Make the filename_raw safe, remove unsupported chars
        filename_con = secure_filename(file_Con.filename)
        # Move the file_Raw form the temporal folder to
        # the upload folder we setup
        file_Con.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_con))

        WebCaseHandler.main()

        age_set = open('HTML_info/age.txt', 'r')
        f = age_set.read()
        if f != '':
            age_info = f.split('[', 1)[0]
            age_offsets = int(f.split("[",1)[1].split(",",1)[0])
            age_offsets_end=int(re.search(r'\d+', f.split(",",1)[1]).group())
        else:
            age_offsets_end = 0
            age_offsets = 0
            age_info = ''

        drug_set = open('HTML_info/drug.txt', 'r')
        drug_info = drug_set.read()

        # gender_set = open('HTML_info/gender.txt', 'r')
        # f = gender_set.read()
        #
        # if f != '[][]' :
        #     gender_offsets = int(re.search(r'\d+', f.split("][", 1)[1].split(",", 1)[0]).group())
        #     gender_offsets_end = int(re.search(r'\d+', f.split("][", 1)[1].split(",",1)[1].split("]",1)[0]).group())
        #     gender_info = f.split("'", 1)[1].split("'",1)[0]
        # else:
        #     gender_info = ''
        #     gender_offsets = 0
        #     gender_offsets_end = 0


        event_set = open('HTML_info/eventdate.txt', 'r')
        f = event_set.read()
        if f != '':
            event_info = f.split('[', 1)[0]
            event_offsets = int(f.split("[", 1)[1].split(",", 1)[0])
            event_offsets_end = event_offsets+str(event_info).__len__()
        else:
            event_info = ''
            event_offsets = 0
            event_offsets_end = 0

        weight_set = open('HTML_info/weight.txt', 'r')
        f = weight_set.read()
        if f != '':
            weight_info = f.split("[",1)[0]
            weight_offsets = int(f.split("[", 1)[1].split(",", 1)[0])
            weight_offsets_end = int(re.search(r'\d+', f.split(",",1)[1]).group())
        else:
            weight_info = ''
            weight_offsets = 0
            weight_offsets_end = 0



        text = open(cwd_uploads + '/' + filename_raw, "r")
        text = text.read()
        return render_template("download.html", text=text, age_info=age_info,
                               drug_info=drug_info, event_info=event_info,
                               weight_info=weight_info,age_offsets=age_offsets,age_offsets_end=age_offsets_end,
                               event_offsets=event_offsets,event_offsets_end=event_offsets_end,
                               weight_offsets=weight_offsets,weight_offsets_end=weight_offsets_end,
                               )


        # return render_template('download.html')


        # return render_template('download.html')
        # downloadfile = filename_raw[0:-4] + '_Intermediate.xml'
        # return redirect(url_for('download_file', filename=downloadfile))

    else:
        return render_template('Error_wrongformat.html'), 403

@app.route('/return-files/')
def return_files():
    f = open("HTML_info/RawName.txt", 'r')
    f = f.read()
    filename = f[0:-4] + '_Intermediate.xml'
    print filename
    downloadfile = "/Users/wutianyu/ISP2016/WebPostProcessing/"
    post = glob.glob(os.path.join(downloadfile, "*.xml"))
    for d in post:
        if filename in d:
            return send_file(d, as_attachment=True)

@app.route('/return-ageset/')
def return_ageset():
    f = open("HTML_info/RawName.txt", 'r')
    f = f.read()
    filename = f[0:-4] + '_AGE_SET_Semifinal.xml'
    downloadfile = "/Users/wutianyu/ISP2016/Test_Suite/Eval_Env/semifinal"
    post = glob.glob(os.path.join(downloadfile, "*.xml"))
    for d in post:
        if filename in d:
            return send_file(d, as_attachment=True)


@app.route('/return-drug/')
def return_drug():
    f = open("HTML_info/RawName.txt", 'r')
    f = f.read()
    filename = f[0:-4] + '_DRUGNAME_Semifinal.xml'
    downloadfile = "/Users/wutianyu/ISP2016/Test_Suite/Eval_Env/semifinal"
    post = glob.glob(os.path.join(downloadfile, "*.xml"))
    for d in post:
        if filename in d:
            return send_file(d, as_attachment=True)


@app.route('/return-eventdate/')
def return_eventdate():
    f = open("HTML_info/RawName.txt", 'r')
    f = f.read()
    filename = f[0:-4] + '_EVENT_DT_Semifinal.xml'
    downloadfile = "/Users/wutianyu/ISP2016/Test_Suite/Eval_Env/semifinal"
    post = glob.glob(os.path.join(downloadfile, "*.xml"))
    for d in post:
        if filename in d:
            return send_file(d, as_attachment=True)


@app.route('/return-gender/')
def return_gender():
    f = open("HTML_info/RawName.txt", 'r')
    f = f.read()
    filename = f[0:-4] + '_SEX_Semifinal.xml'
    downloadfile = "/Users/wutianyu/ISP2016/Test_Suite/Eval_Env/semifinal"
    post = glob.glob(os.path.join(downloadfile, "*.xml"))
    for d in post:
        if filename in d:
            return send_file(d, as_attachment=True)


@app.route('/return-weight/')
def return_weight():
    f = open("HTML_info/RawName.txt", 'r')
    f = f.read()
    filename = f[0:-4] + '_WT_SET_Semifinal.xml'
    downloadfile = "/Users/wutianyu/ISP2016/Test_Suite/Eval_Env/semifinal"
    post = glob.glob(os.path.join(downloadfile, "*.xml"))
    for d in post:
        if filename in d:
            return send_file(d, as_attachment=True)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8089"),
        debug=True
    )
