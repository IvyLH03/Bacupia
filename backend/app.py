from flask import Flask, send_from_directory, abort
from werkzeug.utils import secure_filename, safe_join
from webread import SaveThread
import json
from flask_cors import CORS
from flask import request
import time
from pathlib import Path
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "hello!" 

@app.route('/bacupia/request/<int:post_id>')
def request_backup(post_id):
    request_time = time.time()
    app.logger.info(f'get file | post_id: {post_id} | {request_time} |')
    try: 
        with open('config.json') as f:
            cookies=json.load(f)
        saver = SaveThread(post_id, cookies)
        
        generated_filenames = saver.run_save(save_raw=False, save_minimal=False, simple_filename=True)
        app.logger.info(f'SUCCESS: get file | post_id: {post_id} | {request_time} |')
        # return send_from_directory(
        #     "./saves", generated_filenames[0], as_attachment=True
        # )
        return "Successfully started"
    
    except Exception as err:
        app.logger.info(f'FAILED: get file | post_id: {post_id} | {request_time} |')
        
    
# return all files in save folder
@app.route('/bacupia/archive')
def get_archive():
    # get all files that has been generated
    relative_path = Path("saves/")
    contents = list(relative_path.iterdir())
    all_filenames = []
    for file in contents:
        all_filenames.append(file.name)
    return all_filenames
    # get all files that are in progress

# download a file
@app.route('/bacupia/download/<filename>')
def download_file(filename):
    try:
        # Safely join the folder path and filename to prevent directory traversal
        file_path = safe_join("saves/", filename)

        # Check if the file exists
        if os.path.exists(file_path):
            return send_from_directory("saves/", filename, as_attachment=True)
        else:
            abort(404, description="File not found")

    except Exception as e:
        return str(e)
