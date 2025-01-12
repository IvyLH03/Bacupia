from flask import Flask, send_from_directory
from webread import SaveThread
import json

app = Flask(__name__)

@app.route('/bacupia/<int:post_id>')
def show_post(post_id):
    with open('config.json') as f:
        cookies=json.load(f)
    saver = SaveThread(post_id, cookies)
    saver.run_save("./saves/存档",save_raw=False, save_minimal=False, simple_filename=True)
    return send_from_directory(
        "./saves", "存档.docx", as_attachment=True
    )