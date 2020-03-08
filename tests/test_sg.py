import sys
import os
pwd_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.join(pwd_path, '../')
utils_path = os.path.join(pwd_path,'../codebase/utils')
sys.path.append(parent_path)
sys.path.append(utils_path)
from codebase.utils.tokenizer import Tokenizer
import config

import pkuseg
from minlptokenizer.tokenizer import MiNLPLiteTokenizer
from pyhanlp import *
import hanlp
import thulac	
import codecs

def load_word_dict(path):

    word_freq = {}
    with codecs.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            info = line.split("\t")
            if len(info) < 1:
                continue
            word = info[0]
            # 取词频，默认1
            freq = int(info[1]) if len(info) > 1 else 1
            word_freq[word] = freq
    return word_freq


jieba_tokenizer  = Tokenizer(dict_path=config.word_freq_path, custom_word_freq_dict=load_word_dict(config.custom_word_freq_path))
   
tokenizer_hanlp = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
tokenizer_han = HanLP.newSegment().enableOrganizationRecognize(True)
tokenizer_han.enablePartOfSpeechTagging(False)
tokenizer_mi = MiNLPLiteTokenizer(granularity='fine') # fine：细粒度，coarse：粗粒度
tokenizer_mi1 = MiNLPLiteTokenizer(granularity='coarse') # fine：细粒度，coarse：粗粒度
thu1 = thulac.thulac(seg_only=True)
for text in open("/home/zixiang/DataSets/berttestdata/xiaoaiquerylog/new_domain_session_pairs.txt"):

    print(tokenizer_han.seg(text))

    seg_list = jieba_tokenizer.tokenize(text,mode='default')
    print([i for i in seg_list])# 精确模式
   
    print(tokenizer_mi.cut(text))
    print(tokenizer_mi1.cut(text))
    print(tokenizer_hanlp(text))
    print([i[0] for i in thu1.cut(text)])

    print("+++++++++++++++++++++++++++=")

   