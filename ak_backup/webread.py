import requests
import json
from docx import Document

with open("config.json","r",encoding="utf-8") as f:
    cookies = json.load(f)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
}

client = requests.session()
client.headers = header
client.cookies.update(cookies)




document = Document()
max_page = 110

for i in range(1, max_page + 1):
  payload = {
  "tid":40452148,
  "page":i,
  "authorid":64875447
  }
  res = client.post("https://bbs.nga.cn/app_api.php?__lib=post&__act=list", data=payload)
  data = res.json()
  print(data)

  for post in data['result']:
    content = str(post['content'])
    content = content.replace("<br/>","\n").replace("<div class='dice'>","").replace("</div>","")

    document.add_paragraph(content)
    document.add_paragraph("\n")

document.save("doc.docx")
