# -*- coding: utf-8 -*-
import sys
import os
pwd_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.join(pwd_path, '../')
sys.path.append(parent_path)

from pypinyin import lazy_pinyin
import io
import json
from pyhanlp import *
from tokenizer import Tokenizer
from io_utils import load_json,save_json,load_pkl,dump_pkl
import codecs
import pickle
import threading
from prefix_tree import Trie
from functools import reduce
from re_utils import find_pattern
import config as config

from logger import logger


dict = {}
count = 0

def is_chinese(uchar):
    '''
    @description:  判断一个unicode是否是汉字"
    @param {type} 
    @return:
    '''
    if '\u4e00' <= uchar <= '\u9fa5':
        return True
    else:
        return False

def is_chinese_string(string):
    '''
    @description:  判断是否为汉字
    @param {type} 
    @return:
    '''
    for c in string:
        if not is_chinese(c):
            return False
    return True

def load_word_freq_dict(path):

    word_freq = {}
    with codecs.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            info = line.split()
            if len(info) < 1:
                continue
            word = info[0]
            # 取词频，默认1
            freq = int(info[1]) if len(info) > 1 else 1
            word_freq[word] = freq
    return word_freq

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

def native_content(content):
    '''
    @description: 
    @param {type} 
    @return: content
    '''
    if sys.version_info[0] == 2:
        content = content.decode('utf-8')
    return content

def safe_input(content):
    content = content.strip()
    return native_content(content)

def filelist(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            if not dirs:
                for f in files:
                    yield os.sep.join([root, f])
    else:
        yield path

def get_deletes(word : list) :
    '''
    @description:  对称删除 input list
    @param {type} 
    @return:
    '''
    word = ''.join(lazy_pinyin(word))
    dels = []
    queue = [word]
    dels.append(word)

    for _ in range(2):
        tmp = []
        for word in queue:
            if len(word) > 1:
                for i in range(len(word)):
                    except_char = word[:i] + word[i+1:]
                    if except_char not in dels:
                        dels.append(except_char)
                    if except_char not in tmp:
                        tmp.append(except_char)
        queue = tmp

    return dels

def load_data(fpath):
    '''
    @description: 
    @param {type} 
    @return: 
    '''    
    for fname in filelist(fpath):
        with io.open(fname, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                arr = line.split('\t')[0].split()
        
                if arr:
                    yield safe_input(arr[0])

def cheaksmyspell(symspell_dict,query):
    '''
    @description: 
    @param {type} 
    @return: 
    '''
    tmp_condidate = set()
    deletes = get_deletes(query)

    for d in deletes:
        if d in symspell_dict:
            for i in symspell_dict[d][0]:
                    tmp_condidate.add(i)

    return tmp_condidate 

def cheaksmyspell_apply(x):
    '''
    @description: 
    @param {type} 
    @return: 
    '''
    global count 
    pattern_type = 0
    symspell_dict = load_json("/home/zixiang/Projects/text_correction/codebase/data/symspell_sample_dict.json")
    tmp_condidate = set()
    if find_pattern(x) is not None:
        print(find_pattern(x))
        x , pattern_type = find_pattern(x) 
    deletes = get_deletes(x)

    #查询symspell词典
    for d in deletes:
        if d in symspell_dict:
            for i in symspell_dict[d][0]:
                    tmp_condidate.add(i)
         
    if len(tmp_condidate) == 0:
        return x
    else:
        count += 1
        if pattern_type == 0:
            return str(list(tmp_condidate)[0])
        elif pattern_type == 1:
            return "怎么预防" + str(list(tmp_condidate)[0])
        elif pattern_type == 2:
            return "什么是" + str(list(tmp_condidate)[0])
        elif pattern_type == 3 :
            return str(list(tmp_condidate)[0]) + "怎么预防"
        elif pattern_type == 4 :
            return str(list(tmp_condidate)[0]) + "是什么"
        elif pattern_type == 5 :
            return "播放" + str(list(tmp_condidate)[0]) + "的新闻"

def load_pattern_trie_tree():
    
    trie = Trie()
    for line in open("/home/zixiang/Projects/text_correction/codebase/data/pattern.txt"):
        tmp_pattern = [i for i in line.strip().split("\t")[0]]
        trie.insert(tmp_pattern)

    return trie

def test_pattern_symspell(query:list) -> list: 
    '''
    @description: 使用提取的pattern树对错的句子进行纠错。
    @param {type} 
    @return: 
    '''  
    trie = load_pattern_trie_tree()
    symspell_dict = load_json("/home/zixiang/Projects/text_correction/codebase/data/symspell_dict.json")
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
 
    tmp_condidate = set()
    isword,word_path,pattern = trie.search(query)
    
    #logger.debug("pattern {} wororigin_patternd_path {}".format(pattern,word_path))
    if not isword and len(word_path) ==  0:
        pass
    
    add_flag = True
    origin_words_list = [i for i in word_path.split("*") if i ]
    tmp_string = ""

    for i in pattern:
        if i == "*" :
            if add_flag:
                tmp_string += i
                add_flag = False
        else:
            tmp_string += i
            add_flag = True
    
    origin_pattern = tmp_string.replace("*","{}")

    #logger.debug("origin_pattern {}".format(origin_pattern))
    #logger.debug("origin_word_list {}".format(origin_words_list))
    length = len(origin_words_list)

    
    tmp_list = []
    for i in range(length):
        tmp_list.append([])

    #处理多个位置有错误的情况
    for i in range(length):
        deletes = get_deletes(origin_words_list[i])
        #查询symspell词典
        for d in deletes:
            if d in symspell_dict:
                for j in symspell_dict[d][0]:
                    if j in tmp_list[i]:
                        continue
                    tmp_list[i].append(j)

    if len(tmp_list) == 0:
        return set()

    fn = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
    res = fn(tmp_list)
    
    for line in res:
        tmp_condidate.add((origin_pattern.format(*(line.split(",")))))

    return  list(tmp_condidate)
                
def symspell(input_file,res_dict={}):
    '''
    @description: 
    @param {type} 
    @return: 
    '''    
    count = 0
    for word in load_data(input_file):
        pinyin_word = ''.join(lazy_pinyin(word))
        #print(pinyin_word)
        if pinyin_word in res_dict:
            res_dict[pinyin_word] = [res_dict[pinyin_word][0], res_dict[pinyin_word][1] + 1]
        else:
            res_dict[pinyin_word] = [[], 1]

        if res_dict[pinyin_word][1] == 1:
            # first show of word in corpus
            deletes = get_deletes(word)
            for d in deletes:
                if d in res_dict:
                    res_dict[d][0].append(word)
                    res_dict[d][1] += 1
                   # print(res_dict[d][0],d)
                else:
                    res_dict[d] = [[word], 1]
        count += 1
        if count % 1000 == 0:
            print("count {}".format(count))
        
        if count % 100000 == 0:
            print("save to path")
            break
        
    #print("dict {}".format(dict))
    return res_dict

def clean_dict(input_file,output_path):
    more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']
    res = []
    for i in open(input_file):
        count = 0
        for j in i.strip().split('\t')[0]:
            if j in more_num_str_symbol:
                count += 1

        if count < 2:
            res.append(i)

    with open(output_path, 'w', encoding='utf-8') as f:
        count = 0
        for key in res :
             f.write(key)

        print("save line size:%d to %s" % (count, output_path))


def test():
    '''
    @description:  测试symspell功能
    @param {type} 
    @return:
    '''
    #dict_tmp = symspell("/home/zixiang/ExtraData/xmnlp/tests/sample_words.txt")
    #save_json(dict_tmp,"/home/zixiang/Projects/text_correction/codebase/data/symspell.json")
    
    tmp_dict = load_json(config.new_symspell_json)

    #print("tmp_dict", tmp_dict)
    print(cheaksmyspell(tmp_dict,"小孩同学"))

def multi_threading():
    '''
    @description:  测试symspell功能
    @param {type} 
    @return:
    '''
    stop_words = load_word_freq_dict("/home/zixiang/Projects/text_correction/codebase/data/stopwords.txt")
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    output_path = "/home/zixiang/Projects/text_correction/codebase/data"
    thread_list = []

    for i in range(9):
        thread_list.append(threading.Thread(target=get_symspell_multi_threading, args=(base_path,stop_words,output_path,i)))
    for i in range(9):
        thread_list[i].start()

def get_symspell_multi_threading(base_path,stop_words,output_path,file_index):
    '''
    @description: 多线程模型得到symspell结果
    @param {type} 
    @return:
    ''' 

    #分词
    #Segment = JClass("com.hankcs.hanlp.seg.Segment")
    #Term = JClass("com.hankcs.hanlp.seg.common.Term")

    #tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
    jieba_tokenizer = Tokenizer()
    #HanLP.Config.ShowTermNature = False

    tokenizer = HanLP.newSegment().enableOrganizationRecognize(True)
    #tokenizer.enablePartOfSpeechTagging(False)
    #set_fenci = set()
    dict_fenci = {}
    
    raw_train_paths = os.path.join(base_path,"train/train_" + str(file_index))
    symspell_dic_paths = os.path.join(output_path, "symspell_dic" + str(file_index) + ".txt" )
    
    count = 0
    for sentence in open(raw_train_paths,'r'):
    
        #长度小于4
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        if len(sentence) <= 4 :
            if sentence not in dict_fenci :
                dict_fenci[sentence] = 1
            else:
                dict_fenci[sentence] += 1

            continue

        #分词
        for j in [i[0] for i in jieba_tokenizer.tokenize(sentence)]:
            if j not in stop_words and len(j) >= 2 :
                if j not in dict_fenci:
                    dict_fenci[j] = 1
                else:
                    dict_fenci[j] += 1
        
        if count % 10000 == 0:
            print("thread {}  count {}".format(file_index,count))
            print("thread {} dict len {}".format(file_index,len(dict_fenci)))
        count += 1 

    #ner
    count = 0
    for sentence in open(raw_train_paths,'r'):      
    
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        for j in [str(i.word) for i in tokenizer.seg(sentence)]:
            if j not in stop_words and len(j) >= 2 :
                if j not in dict_fenci :
                    dict_fenci[j] = 1
                else:
                    dict_fenci[j] += 1

        if count % 10000 == 0:
            print("thread {}  count {}".format(file_index,count))
            print("thread {} dict len {}".format(file_index,len(dict_fenci)))
        count += 1 

    with open(symspell_dic_paths, 'w', encoding='utf-8') as f:
        count = 0
        tmp_res = []
        list1 = sorted(dict_fenci.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1:
             f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, symspell_dic_paths))

def update_symspell_dict(input_file,output_file):

    '''
    @description: 得到symspell key-value词典
    @param {type} 
    @return:
    '''
    dict_tmp = symspell(input_file = input_file,res_dict = load_json("/home/zixiang/Projects/text_correction/codebase/data/symspell_dict.json"))
    save_json(dict_tmp,output_file)

def update_dcit(input_file_list):
    '''
    @description:  得到symspell text结果,使用了停用词典
    @param {type} 
    @return:
    '''
    res_dict = {}
    count = 0
    for f in input_file_list:
        for i in open(os.path.join(config.output_path,f)):
            #print(i.strip().split('\t'))
            #print(line)
            tmp_list = i.strip().split('\t')
            #print(tmp_list)
            word = tmp_list[0]
            nu = tmp_list[1]

            count += 1
            nu = int(nu)
            if word not in res_dict:
                res_dict[word]  = nu
            else:
                res_dict[word] += nu

            if count % 1000 == 0:
                print("count",count)
            
    with open(config.new_symspell_dict_paths, 'w', encoding='utf-8') as f:
        count = 0
        tmp_res = []
        list1 = sorted(res_dict.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1:
             f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, config.new_symspell_dict_paths))

def get_symspell_dict():
    '''
    @description:  得到symspell text结果,使用了停用词典
    @param {type} 
    @return:
    '''
    jieba_tokenizer  = Tokenizer(dict_path=config.word_freq_path, custom_word_freq_dict=load_word_dict(config.custom_word_freq_path))
    tokenizer = HanLP.newSegment().enableOrganizationRecognize(True)

    dict_fenci = {}
    
    stop_words = load_word_freq_dict(config.stopwords_path)
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    output_path = "/home/zixiang/Projects/text_correction/codebase/data"
    
    raw_train_paths = os.path.join(base_path,"new_domain_session_pairs.txt")
    symspell_dic_paths = os.path.join(output_path, "new_domain_session_pairs_4symspell_dict.txt")

    count = 0
    len_count = 0
    for sentence in open(raw_train_paths,'r'):
        #长度小于4
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        if len(sentence) <= 4 :
            len_count += 1
            if sentence not in dict_fenci :
                dict_fenci[sentence] = 1
            else:
                dict_fenci[sentence] += 1
            continue

        #分词
        for j in [i[0] for i in jieba_tokenizer.tokenize(sentence)]:
            if j not in stop_words and len(j) >= 2 :
                if j not in dict_fenci:
                    dict_fenci[j] = 1
                else:
                    dict_fenci[j] += 1
        
        if count % 10000 == 0:
            print("count {}".format(count))
            print("dict len {}".format(len(dict_fenci)))
        count += 1 

    #ner
    count = 0
    for sentence in open(raw_train_paths,'r'):      
    
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        for j in [str(i.word) for i in tokenizer.seg(sentence)]:
            if j not in stop_words and len(j) >= 2 :
                if j not in dict_fenci :
                    dict_fenci[j] = 1
                else:
                    dict_fenci[j] += 1

        if count % 10000 == 0:
            print("count {}".format(count))
            print("len_count {}".format(len_count))
            print("dict len {}".format(len(dict_fenci)))
        count += 1 

    with open(symspell_dic_paths, 'w', encoding='utf-8') as f:
        count = 0
        tmp_res = []
        list1 = sorted(dict_fenci.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1:
             f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, symspell_dic_paths))

def get_symspell_dict_key_value(input_file,output_file):
    '''
    @description: 得到symspell key-value词典
    @param {type} 
    @return:
    '''
    dict_tmp = symspell(input_file)
    save_json(dict_tmp,output_file)
    
    # tmp_dict = load_json("/home/zixiang/Projects/text_correction/codebase/data/symspell_dict.json")
    # print("tmp_dict", tmp_dict)
    # print(cheaksmyspell(dict_tmp,"小孩同学"))

def get_tmp_result():
    global count 
    tmp_dict = load_json("/home/zixiang/Projects/text_correction/codebase/data/symspell_dict.json")
    print("symspell_dict loaded")
    #print("tmp_dict", tmp_dict)
    #print(cheaksmyspell(tmp_dict,"新兴肥业"))
    import pandas as pd

    df = pd.read_excel("/home/zixiang/Downloads/热词评测20200123.xlsx",sheet_name=2)

    #print(df["query"])
    df["new_result"] = df["query"].apply(cheaksmyspell_apply)

    print(df.head())
    df.to_excel("/home/zixiang/Downloads/热词评测20200123_new.xlsx",index=None,columns=["query","rewrite_query","new_result"],encoding="utf_8")
    print("count 影响面",count)

def update_pipeline():

    input_file_list = ['new_domain_session_pairs_ner.txt','new_domain_session_pairs_4symspell_dict.txt','symspell_dict.txt']
    #get_symspell_dict()
    #update_dcit(input_file_list)
    clean_dict(config.new_symspell_dict_paths,config.new_clean_symspell_dict_paths)
    #update_symspell_dict(config.new_clean_symspell_dict_paths,config.new_symspell_json)
    

if __name__ == "__main__":
    #test()
    #multi_threading()

    # input_file = "/home/zixiang/Projects/text_correction/codebase/data/symspell_dict.txt"
    # output_file = "/home/zixiang/Projects/text_correction/codebase/data/symspell_dict.json"
    # set_symspell_dict(input_file,output_file)

    # test get_tmp_result
    # input_file = "/home/zixiang/Projects/text_correction/codebase/data/sample_words.txt"
    # output_file = "/home/zixiang/Projects/text_correction/codebase/data/symspell_sample_dict.json"
    # set_symspell_dict(input_file,output_file)
    # get_tmp_result()
    # test_query = "怎 么 样 预 防 武 汉 心 型 病 毒".strip().split()
    # test_query = "怎 么 样 预 防 武 汉 心 型 病 毒 也 就 是 冠 状 病 毒 呢".strip().split()
    
    # res = test_pattern_symspell(test_query)
    # print(res)

    #update_pipeline()
    test()