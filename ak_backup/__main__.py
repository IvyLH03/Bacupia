from webread import SaveThread
import json
import os

cookies = {}
try:
  cookies['ngaPassportCid'] = os.environ['ngaPassportCid']
  cookies['ngaPassportUid'] = os.environ['ngaPassportUid']
except KeyError as e:
  print(e)

saver = SaveThread(40452148, 64875447, cookies)
saver.run_save("百命海猎/百命海猎")