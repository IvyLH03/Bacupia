from typing import List
import requests
import json
from docx import Document
import re
import html
import time
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt

class Post:
    x:int

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
    def get_page_posts(self, pgnum: int) -> List[object]:
        return self.get_page(pgnum)['result']

    # 获取整个帖子的回复列表
    def get_thread_posts(self) -> List[object]:
        pgnum = self.get_thread_pgnum()
        posts = []
        for i in range(1, self.max_page + 1):
            print("fetching posts from page", i, "/", self.max_page, "...")
            posts += (self.get_page_posts(i))
        return posts
            

    # 处理一条回复的文字部分, 生成用于排版的纯文字
    def process_post_content_minimal(self, content: str) -> str:
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
        for i in range(0, len(content_list)):
            if len(content_list[i]) > 0:
                content += content_list[i] + "\n"

        return content #.strip()
    
    # 处理一条回复的文字部分，生成阅读格式
    def add_post_to_doc_reading(self, post:Post, ref):
        print("TODO")

    # 生成文档
    def run_save(self, thread_name:str, save_raw=True, save_minimal=True, save_reading=True):
        posts = self.get_thread_posts()
        time_suffix = time.strftime("%Y%m%d_%H%M%S")
        if save_raw:
            filename = thread_name + "_raw_" + time_suffix + ".json"
            self.save_raw(posts, filename)
        if save_minimal:
            filename = thread_name + "_minimal_" + time_suffix + ".docx"
            self.save_minimal(posts, filename)
        if save_reading:
            print("TODO")
    
    # 保存所有回帖的json数据文件
    def save_raw(self, posts:List[object], filename:str):
        print("saving raw to", filename, "...")
        with open(filename,"w",encoding="utf-8") as f:
            json.dump(posts, f)
        print("raw saved!")

            
    # 保存所有回帖的排版文档
    def save_minimal(self, posts:List[object], filename:str):
        print("saving minimal to", filename, "...")
        document = Document()
        style = document.styles.add_style('ThreadMinimal', WD_STYLE_TYPE.PARAGRAPH)
        paragraph_format = style.paragraph_format
        paragraph_format.space_after = Pt(0)
        for post in posts:
            content = self.process_post_content_minimal(str(post['content']))
            if len(content) > 0:
                paragraph = document.add_paragraph(content)
                paragraph.style = document.styles['ThreadMinimal']
        document.save(filename)
        print("minimal saved!")

    # 保存所有回帖的阅读格式文档
    def save_reading(self, posts:List[object], filename:str):
        print("saving reading to", filename, "...")
        # TODO: GET THIS DONE

if __name__ == "__main__":
    saver = SaveThread(40452148, 64875447)
    thread_name = "./out/百命海猎"
    # saver.run_save(thread_name=thread_name, save_raw=True, save_minimal=False, save_reading=False)
    with open("./out/百命海猎_raw_20240909_131332.json") as f:
        posts = json.load(f)
    time_suffix = time.strftime("%Y%m%d_%H%M%S")
    filename = thread_name + "_minimal_" + time_suffix + ".docx"
    saver.save_minimal(posts, filename)