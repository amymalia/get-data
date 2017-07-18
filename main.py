"""
Thrilling location to send RESTful pushes

"""



import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

import sys
import cloudstorage as gcs
from google.appengine.api import app_identity

ALLOWED_EXTENSIONS = set(['txt', 'kml'])

app = Flask(__name__)
app.debug = True

# checks file is in allowed file list
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/endpoint', methods=['POST'])
def create_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'result': 'no file part'})
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return jsonify({'result': 'no selected file'})
    if file and allowed_file(file.filename):
        bucket_name = os.environ.get('BUCKET_NAME',
                                     'test-push-172208.appspot.com')
        bucket = '/' + bucket_name
        filename = secure_filename(file.filename)
        filePath = bucket + '/' + filename
        # googlePath = 'https://storage.googleapis.com/' + filePath
        googlePath = 'https://developers.google.com/maps/documentation/javascript/examples/kml/westcampus.kml'
        try:
            write_retry_params = gcs.RetryParams(backoff_factor=1.1)
            gcs_file = gcs.open(filePath,
                                'w',
                                content_type='text/plain',
                                options={'x-goog-meta-foo': 'foo',
                                         'x-goog-meta-bar': 'bar'},
                                retry_params=write_retry_params)
            gcs_file.write(file.read())
            gcs_file.close()
            return jsonify({'result': 'ok'})

        except Exception, e:
            logging.exception(e)
            return jsonify({'result': 'not too good'})

@app.route('/', methods=['POST','GET'])
def display_file():
    if request.method == 'POST':
        return render_template('map.html', googlePath='https://storage.googleapis.com/'+request.form['map'])
    else:
        bucket_name = os.environ.get('BUCKET_NAME',
                                     'test-push-172208.appspot.com')
        bucket = '/' + bucket_name
        files = gcs.listbucket(bucket, max_keys=20)
        return render_template('picker.html', files=files)
