from flask import Flask, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename, safe_join
from webread import SaveThread
import json
from flask_cors import CORS
from flask import request
import time
from pathlib import Path
import os
import asyncio
from tasks import run_save_task
from celery.result import AsyncResult

app = Flask(__name__)
CORS(app)

# make a backup request
@app.route('/bacupia/request/<int:tid>')
async def request_backup(tid):
    request_time = time.time()
    app.logger.info(f'get file | post_id: {tid} | {request_time} |')
    try: 
        task = run_save_task.delay(tid)
        ret = {
            "msg": "Successfully started",
            "task_id": task.id
        }
        return jsonify(ret)
    
    except Exception as err:
        app.logger.info(f'FAILED: get file | post_id: {tid} | {request_time} |')
        response = {
            "error": "Internal Server Error",
            "message": str(err) if str(err) else "An unexpected error occurred."
        }
        return jsonify(response), 500
        
    
# return all files in save folder
@app.route('/bacupia/archive')
def get_archive():
    # get all files that has been generated
    relative_path = Path("saves/")
    contents = list(relative_path.iterdir())
    all_filenames = []
    for file in contents:
        all_filenames.append({
            "name": file.name,
            "time": file.stat().st_ctime
        })
    return jsonify(all_filenames)
    
# check status of a task
@app.route('/bacupia/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task_result = AsyncResult(task_id)  # Get task by ID
    if task_result.state == "PENDING":
        response = {"state": "PENDING"}
    elif task_result.state == "PROGRESS":
        response = {"state": "PROGRESS"}
    elif task_result.state == "SUCCESS":
        response = {"state": "SUCCESS"}
    else:
        response = {"state": task_result.state}
    return jsonify(response)


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
