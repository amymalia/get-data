"""
Thrilling location to send RESTful pushes

"""



import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory

import sys
#sys.path.append('/home/sam/gcloud/python-docs-samples/appengine/standard/storage/appengine-client/lib/')

#import cloudstorage as gcs

UPLOAD_FOLDER = '/home/amytakayesu/get-data/'
ALLOWED_EXTENSIONS = set(['txt', 'kml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

# checks file is in allowed file list
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # write_retry_params = gcs.RetryParams(backoff_factor=1.1)
            # gcs_file = gcs.open('mwahah.txt',
            #                     'w',
            #                     content_type='text/plain',
            #                     options={'x-goog-meta-foo': 'foo',
            #                             'x-goog-meta-bar': 'bar'},
            #                     retry_params=write_retry_params)
            # gcs_file.write('abcde\n')
            # gcs_file.write('f'*1024*4 + '\n')
            # gcs_file.close()
            return jsonify({'result':'ok'})
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return '''
    <!doctype html>
    <title>HOTMAP</title>
    <h1>Awesome File Uploader!</h1>
    <h2>what have you got?</h2>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)