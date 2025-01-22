from celery import Celery
import json
from webread import SaveThread

app = Celery('tasks', backend='redis://localhost', broker='amqp://localhost')

def init():
    global cookies
    with open('config.json') as f:
      cookies = json.load(f)

@app.task
def add(x, y):
    return x + y

@app.task
def run_save_task(tid):
  saver = SaveThread(tid, cookies, debug=True)
  saver.run_save(save_raw=False, save_minimal=False)
  
init()