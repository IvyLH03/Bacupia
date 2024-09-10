from webread import SaveThread
import json
import os

cookies = {}
try:
  cookies['ngaPassportCid'] = os.environ['ngaPassportCid']
  cookies['ngaPassportUid'] = os.environ['ngaPassportUid']
except KeyError as e:
  with open('config.json') as f:
    cookies=json.load(f)

saver = SaveThread(40452148, 64875447, cookies)
saver.run_save("./saves/百命海猎")