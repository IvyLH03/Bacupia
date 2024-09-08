from typing import List
import requests
import json
from docx import Document
import re
import html
import time

class SaveThread:
    def __init__(self, tid: int, authorid: int):
        self.tid = tid
        self.authorid = authorid
        self.max_page = self.get_thread_pgnum()

    def load_cookies():
        with open("config.json","r",encoding="utf-8") as f:
            return json.load(f)

    client = requests.session()
    client.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    }
    client.cookies.update(load_cookies())


    # 获取一页帖子的json
    def get_page(self, pgnum: int):
        payload = {
            "tid":self.tid,
            "page":pgnum,
            "authorid":self.authorid
        }
        res = self.client.post("https://bbs.nga.cn/app_api.php?__lib=post&__act=list", data=payload)
        return res.json()

    # 获取一个帖子的页数
    def get_thread_pgnum(self):
        return self.get_page(1)['totalPage']

    # 获取一页帖子的回复列表
    def get_page_posts(self, pgnum: int) -> List[str]:
        return self.get_page(pgnum)['result']

    # 处理一条回复的文字部分
    def process_post_content(self, content: str) -> str:
        # 删除html标签
        content = content.replace("<br/>","\n")
        content = re.sub('<[^<]+?>', '', content)
        content = html.unescape(content)

        # 跳过回复楼层
        if content.__contains__("Reply to"):
            return ""

        # 替换unicode字符
        def subchr(s):
            return chr(int(s.group(1)))
        content = re.sub('&#([0-9]+);',subchr,content)

        # 检测重复d2
        content_list = content.split("\n")
        # ROLL : d10
        # ROLL : d2
        for i in range(0, len(content_list) - 1):
            prev_item = content_list[i]
            cur_item = content_list[i+1]
            # 如果第i条是d10且出目不是10，同时第i+1条是d2，则删除d2
            if prev_item.startswith("ROLL : d10") and cur_item.startswith("ROLL : d2") and (not prev_item.startswith("ROLL : d10=d10(10)=10")):
                content_list[i+1] = ""

        # 重新组合结果
        content = ""
        for item in content_list:
            if len(item) > 0:
                content += item + "\n"

        return content

    def run_save(self, filename: str):
        document = Document()
        for i in range(1, self.max_page + 1):
            print("saving page",i,"/",self.max_page,"...")
            post_list = self.get_page_posts(i)
            for post in post_list:
                content = self.process_post_content(str(post['content']))
                if len(content) > 0:
                    document.add_paragraph(content)
        document.save(filename)
    

    # for i in range(1, max_page + 1):
    #     print("saving page",i,"...")
    #     payload = {
    #     "tid":40452148,
    #     "page":i,
    #     "authorid":64875447
    #     }
    #     res = client.post("https://bbs.nga.cn/app_api.php?__lib=post&__act=list", data=payload)
    #     data = res.json()
    #     #print(data)

    #     for post in data['result']:
    #         content = str(post['content'])

    #         # 删除html标签
    #         # content = content.replace("<div class='dice'>","").replace("</div>","").replace("<b>","").replace("</b>","")
    #         content = content.replace("<br/>","\n")
    #         content = re.sub('<[^<]+?>', '', content)
    #         content = html.unescape(content)

    #         # 替换unicode字符
    #         def subchr(s):
    #             return chr(int(s.group(1)))
    #         content = re.sub('&#([0-9]+);',subchr,content)

    #         # 跳过回复楼层
    #         if content.__contains__("Reply to"):
    #             continue

    #         # 检测重复d2
    #         content_list = content.split("\n")
    #         # ROLL : d10
    #         # ROLL : d2
    #         for i in range(0, len(content_list) - 1):
    #             prev_item = content_list[i]
    #             cur_item = content_list[i+1]
    #             # 如果第i条是d10且出目不是10，同时第i+1条是d2，则删除d2
    #             if prev_item.startswith("ROLL : d10") and cur_item.startswith("ROLL : d2") and (not prev_item.startswith("ROLL : d10=d10(10)=10")):
    #                 content_list[i+1] = ""

    #         fin_content = ""
    #         for item in content_list:
    #             if len(item) > 0:
    #                 fin_content += item + "\n"
                
    #         document.add_paragraph(fin_content)

    # document.save("backup_20240907_noHtmlTags.docx")

if __name__ == "__main__":
    saver = SaveThread(40452148, 64875447)
    filename = "backup_" + time.strftime("%Y%m%d_%H%M%S") + ".docx"
    print(filename)
    saver.run_save("./out/"+filename)