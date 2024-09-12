import json
import matplotlib.pyplot as plt
import numpy as np
from typing import List
import re

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


if __name__ == "__main__":
  stats = Stats()
  stats.load_data("./out/processed_test_0.json")

  dices = []

  for i in range(len(stats.posts)):
    #print(stats.posts[i])
    dices += stats.get_post_dices(stats.posts[i])

  argue = {}

  for dice in dices:
    rematch = re.match("(.+)的出力",dice.immi_desc)
    if rematch != None:
      name = rematch[1]
      if(not argue.__contains__(name)):
        argue[name]=[]
      argue[name].append(dice)
    
  argue_sorted = dict(sorted(argue.items(), key=lambda item: len(item[1]), reverse=True))
  for key in argue_sorted:
    print(key,": ", len(argue_sorted[key]), "次", sep='', end=" ")
    print("平均:", end='')
    tot = 0
    for dice in argue_sorted[key]:
      tot += dice.result
    print(tot/len(argue_sorted[key]))
  
  keywords = [""]
  stat_arr = []
  for dice in argue_sorted['Ishar-mla']:
    stat_arr.append(dice.result)


  # stat_arr = []
  # num_d100 = 0
  # freq_d100 = {}

  # for dice in dices:
  #   if(dice.maxbound == 100):
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
  fig, ax = plt.subplots()

  ax.hist(stat_arr,bins=5)

  ax.set(xlim=(1, 100))

  plt.show()