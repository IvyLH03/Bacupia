import json
import matplotlib.pyplot as plt
import numpy as np
from typing import List
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Dice_result:
  def __init__(self, maxbound, result, immi_desc = ""):
    self.maxbound = maxbound
    self.result = result
    self.immi_desc = immi_desc

class Stats:
  def __init__(self):
    pass

  def load_data(self, path:str):
    with open(path) as f:
      self.posts = json.load(f)

  def get_post_dices(self, post) -> List[Dice_result]:
    dices = []
    for i in range(len(post['content'])):
      content = str(post['content'][i])
      if content.startswith("ROLL : "):
        rematch = re.search('d[\d+]+=d(\d+)\((\d+)\)',content)
        #print(rematch[1],rematch[2])
        dices.append(Dice_result(maxbound=int(rematch[1]),result=int(rematch[2]),immi_desc=post['content'][i-1]))
    return dices
  
  def get_post_segs(self, post) -> List[str]:
    segs = []
    for content in post['content']:
      segs += jieba.cut(content)
    return segs

  def get_all_freq(self) -> dict:
    word_freq = {}
    for post in self.posts:
      segs = self.get_post_segs(post)
      for seg in segs:
        if not word_freq.__contains__(seg):
          word_freq[seg] = 0
        word_freq[seg] += 1
    return word_freq
  


  def get_interval_freq(self, start:int, end:int, skips = [], ignore_words = [], ignore_num=False, ignore_d=False) -> dict:
    word_freq = {}
    for post in self.posts:

      if(int(post["lou"]) < start):
        continue
      if(int(post["lou"]) > end):
        break

      flag = False
      for skip in skips:
        if post["lou"] >= skip[0] and post["lou"] <= skip[1]:
          flag = True
          break
      if(flag):
        continue

      segs = self.get_post_segs(post)
      for seg in segs:
        if seg in ignore_words:
          continue

        if(ignore_num):
          try:
            int(seg)
            continue
          except:
            pass

        if(ignore_d and seg[0]=='d'):
          continue

        if seg not in word_freq:
          word_freq[seg] = 0
        word_freq[seg] += 1
    return word_freq
  


if __name__ == "__main__":
  iters = [[2, 19], [20, 93], [94, 133], [134, 137], [138, 602], 
           [603, 686], [696, 843], [844, 1050], [1084, 1155], [1156, 1330], 
           [1487, 1580], [1581, 1660], [1661, 1742], [1744, 1842], [1932, 2309], ]
  skip = [[609, 638], [2033, 2049]]

  ignores = []
  with open("stopwords.txt") as f:
    for line in f:
      if(line[len(line)-1 == '\n']):
        line = line[:len(line)-1]
      ignores.append(line)
    print(ignores)

  jieba.load_userdict("dict.txt")

  stats = Stats()
  stats.load_data("./out/processed_test_0.json")

  
  index = 0
  for iter in iters:
    print(iter)
    word_freq = stats.get_interval_freq(iter[0], iter[1], skips=skip, ignore_words=ignores, ignore_num=True, ignore_d=True)
    word_freq_sorted = dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True))
    j = 0
    for i in word_freq_sorted:
      j += 1
      if(j > 500) or word_freq_sorted[i] == 3:
        break 
      print(i, word_freq_sorted[i])

    index+=1
    wordcloud_title = "wordcloud_"+str(index)+".png"
    
    wordcloud = WordCloud(font_path="FangZhengHeiTiJianTi-1.ttf",width = 800, height = 800, max_words=50).generate_from_frequencies(word_freq_sorted)

    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    
    #plt.show()
    plt.savefig(wordcloud_title)

    
  # dices = []

  # for i in range(len(stats.posts)):
  #   #print(stats.posts[i])
  #   dices += stats.get_post_dices(stats.posts[i])


  # argue = {}

  # for dice in dices:
  #   rematch = re.match("(.+)的出力",dice.immi_desc)
  #   if rematch != None:
  #     name = rematch[1]
  #     if(not argue.__contains__(name)):
  #       argue[name]=[]
  #     argue[name].append(dice)
    
  # argue_sorted = dict(sorted(argue.items(), key=lambda item: len(item[1]), reverse=True))
  # for key in argue_sorted:
  #   print(key,": ", len(argue_sorted[key]), "次", sep='', end=" ")
  #   print("平均:", end='')
  #   tot = 0
  #   for dice in argue_sorted[key]:
  #     tot += dice.result
  #   print(tot/len(argue_sorted[key]))
  
  # keywords = [""]
  # stat_arr = []
  # for dice in argue_sorted['Ishar-mla']:
  #   stat_arr.append(dice.result)


  # stat_arr = []
  # num_d100 = 0
  # freq_d100 = {}

  # for dice in dices:
  #   #if(dice.maxbound == 100):
  #   if(dice.immi_desc.startswith("海域安全性")):
    
  #     stat_arr.append(dice.result)
  #     num_d100+=1
  #     if(freq_d100.__contains__(dice.result)):
  #       freq_d100[dice.result]+=1
  #     else:
  #       freq_d100[dice.result]=1
  # print("Total:",len(dices),"\nd100:",num_d100)
  # sorted = dict(sorted(freq_d100.items(), key=lambda item: item[1], reverse=True))
  # j = 1
  # for i in sorted:
  #   print("#",j,"  d100=", i, ": ",sorted[i],"次",sep='')
  #   j+=1
  # # plot:
  # fig, ax = plt.subplots()

  # ax.hist(stat_arr,bins=20)

  # #ax.set(xlim=(1, 100), ylim=(0,8))

  # plt.show()