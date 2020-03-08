# -*- coding: utf-8 -*-
import sys
import os
pwd_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.join(pwd_path, '../')
utils_path = os.path.join(pwd_path,'../codebase/utils')
sys.path.append(parent_path)
sys.path.append(utils_path)

from codebase.detector import Detector
from codebase.utils.tokenizer import segment
from codebase.corrector import Corrector

error_sentences = [
    '这个跟 原木纯品 那个啥区别？不是原木纸浆做的？',
    '能充几次呢？',
    '这是酸奶还是像饮料一样的奶？',  # [['像', '想', 6, 7]])
    '现在银色的K2P是MTK还是博通啊？',  # [['博通', '拨通', 14, 16]])
    '是浓稠的还是稀薄的？',
    '这个到底有多辣？',  # [['有多辣', '有多拉', 4, 7]])
]

text = '这个到底有多辣？'
error_sentence_3 = [
        '小孩同学',
        '降低小孩声音',
        '青铜设置',
        '鳄鱼细不细恐龙',
        '你真是能源小便 ',
        '我是刚重音乐出来的',
        '给我查一下先内的近义词',
        '小爱同学打开吃翻译',
        '你千遍',
        '长沙建',
        '防疫受校长',
        '小爱明天中午提醒我去图书馆作为省',
        '五点石响铃',
        '百度搜索我爱你'
        ]
error_sentence_3 = [
        '巨蛇',
        '我想杀人',
        '篮球的英文',
        '播放睡眠歌曲',
        '打开微信读书 ',
        '大哥火山小视频',
        '小爱同学我丢你妈',
        '无',
        '帮我百度支付毕加索的画',

        ]
d = Detector()
print(d.ppl_score("胡一天演过什么电视剧"))

for i in error_sentence_3:
    print(i)
    print(d.ppl_score([x for x in i]))

 
# def test_ars_correct(path):
#     count = 0
#     res = 0
#     for i in open(path):
#         item = i.strip().split("\t")
#         res += d.ppl_score([x for x in item[1]])
#         count += 1
#     print(count,res//count)


# test_ars_correct("/home/zixiang/Projects/text_correction/codebase/data/test_data.txt")