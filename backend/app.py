from flask import Flask, send_from_directory
from webread import SaveThread
import json
from flask_cors import CORS
from flask import request
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "hello!" 

@app.route('/bacupia/<int:post_id>')
def show_post(post_id):
    request_time = time.time()
    app.logger.info(f'get file | post_id: {post_id} | {request_time} |')
    try: 
        with open('config.json') as f:
            cookies=json.load(f)
        saver = SaveThread(post_id, cookies)
        generated_filenames = saver.run_save(save_raw=False, save_minimal=False, simple_filename=True)
        app.logger.info(f'SUCCESS: get file | post_id: {post_id} | {request_time} |')
        return send_from_directory(
            "./saves", generated_filenames[0], as_attachment=True
        )
    
    except Exception as err:
        app.logger.info(f'FAILED: get file | post_id: {post_id} | {request_time} |')
        
    
    