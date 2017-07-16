"""
Thrilling location to send RESTful pushes

"""



import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory

import sys
#sys.path.append('/home/sam/gcloud/python-docs-samples/appengine/standard/storage/appengine-client/lib/')

import cloudstorage as gcs
from google.appengine.api import app_identity

UPLOAD_FOLDER = '/home/amytakayesu/get-data/'
ALLOWED_EXTENSIONS = set(['txt', 'kml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

# checks file is in allowed file list
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#[START delete_files]
# def delete_files(self):
#     self.response.write('Deleting files...\n')
#     for filename in self.tmp_filenames_to_clean_up:
#       self.response.write('Deleting file %s\n' % filename)
#       try:
#         gcs.delete(filename)
#       except gcs.NotFoundError:
#         pass
#[END delete_files]

@app.route('/', methods=['GET', 'POST'])
def create_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return jsonify({'result': 'no file part'})
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return jsonify({'result': 'no selected file'})
        if file and allowed_file(file.filename):
            # bucket_name = os.environ.get('BUCKET_NAME',
            #                              app_identity.get_default_gcs_bucket_name())
            bucket_name = os.environ.get('BUCKET_NAME',
                                         'test-push-172208.appspot.com')
            bucket = '/' + bucket_name
            filename = secure_filename(file.filename)
            filePath = bucket + '/' + filename
            #self.tmp_filenames_to_clean_up = []
            try:
                #filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                write_retry_params = gcs.RetryParams(backoff_factor=1.1)
                gcs_file = gcs.open(filePath,
                                    'w',
                                    content_type='text/plain',
                                    options={'x-goog-meta-foo': 'foo',
                                             'x-goog-meta-bar': 'bar'},
                                    retry_params=write_retry_params)
                gcs_file.write(file.read())
                #gcs_file.write('f' * 1024 * 4 + '\n')
                gcs_file.close()
                #self.tmp_filenames_to_clean_up.append(filename)
                return jsonify({'result': 'ok'})

            except Exception, e:
                logging.exception(e)
                return jsonify({'result': 'not too good'})
                #self.delete_files()
                #self.response.write('\n\nThere was an error running the demo! '
                                    #'Please check the logs for more details.\n')

            #else:
                #self.delete_files()
                #self.response.write('\n\nThe demo ran successfully!\n')

            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    else:
        return render_template('map.html')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)
