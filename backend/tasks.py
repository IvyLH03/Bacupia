from celery import Celery
import json
from webread import SaveThread

app = Celery('tasks', backend='redis://localhost', broker='amqp://localhost')

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_backend="redis://localhost",  
)

def init():
    global cookies, base_path
    with open('config.json') as f:
      data = json.load(f)
      cookies = data["cookies"]
      base_path = data["basePath"]


@app.task(name='tasks.run_save_task')
def run_save_task(tid):
  saver = SaveThread(tid, cookies, debug=True, base_path=base_path)
  filenames = saver.run_save(save_raw=False, save_minimal=False, filename_timestamp=False)
  return filenames
  
init()