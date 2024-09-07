import requests
import json
from docx import Document


def load_cookies():
    with open("config.json","r",encoding="utf-8") as f:
        return json.load(f)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
}

client = requests.session()
client.headers = header
client.cookies.update(load_cookies())

document = Document() 
max_page = 110 # TODO: don't hardcode

for i in range(1, max_page + 1):
    print("saving page",i,"...")
    payload = {
    "tid":40452148,
    "page":i,
    "authorid":64875447
    }
    res = client.post("https://bbs.nga.cn/app_api.php?__lib=post&__act=list", data=payload)
    data = res.json()
    #print(data)

    for post in data['result']:
        content = str(post['content'])

        content = content.replace("<div class='dice'>","").replace("</div>","").replace("<b>","").replace("</b>","")

        # 跳过回复楼层
        if content.__contains__("Reply to"):
            continue

        # 检测重复d2
        content_list = content.split("<br/>")
        # ROLL : d10
        # ROLL : d2
        for i in range(0, len(content_list) - 1):
            prev_item = content_list[i]
            cur_item = content_list[i+1]
            # 如果第i条是d10且出目不是10，同时第i+1条是d2，则删除d2
            if prev_item.startswith("ROLL : d10") and cur_item.startswith("ROLL : d2") and (not prev_item.startswith("ROLL : d10=d10(10)=10")):
                content_list[i+1] = ""

        fin_content = ""
        for item in content_list:
            if len(item) > 0:
                fin_content += item + "\n"
            
        document.add_paragraph(fin_content)

document.save("backup_20240907_noUselessD2.docx")