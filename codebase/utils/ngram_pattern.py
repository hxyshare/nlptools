# -*- coding: utf-8 -*-
'''
# Created on Feb-26-20 10:43
# @author: huazixiang
'''
import os

thread_hold = 900000
ngram_list = []
order_n_gram_dict = {}

def get_order_n_gram(sentence):
    #sentence = sentence.split()
    
    length = len(sentence)
    order_n_gram_dict = {}
    for i in range(length):
        for j in range(i + 1,length):
            tmp_string  = sentence[i] + sentence[j]
            if tmp_string not in order_n_gram_dict:
                order_n_gram_dict[tmp_string] = 1
            else:
                order_n_gram_dict[tmp_string] += 1
            for k in range(j + 1,length):
                tmp_string  = sentence[i] + sentence[j] + sentence[k]
                if tmp_string not in order_n_gram_dict:
                    order_n_gram_dict[tmp_string] = 1
                    
                else:
                    order_n_gram_dict[tmp_string] += 1

    return order_n_gram_dict
    

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


def get_pattern_dict_fixed(ngram=3):
    '''
    @description:  得到pattern分词结果,没有停用词典
    @param {type} 
    @return:
    '''

    #order_n_gram_dict = {}
    
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    output_path = "/home/zixiang/Projects/text_correction/codebase/data"
    
    raw_train_paths = os.path.join(base_path,"xiaoai_v2.txt")
    symspell_dic_paths = os.path.join(output_path, "pattern_dict_4gram_fixed.txt")

    count = 0
    for sentence in open(raw_train_paths,'r'):
      
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        sentence = [i for i in sentence]
        #length = len(sentence)

        get_ngram(sentence,0,"",ngram)
        #print(order_n_gram_dict)

        if count % 10000 == 0:
            print("count {}".format(count))
            #print("order_n_gram_dict",order_n_gram_dict)
            print("dict len {}".format(len(order_n_gram_dict)))
        count += 1 

        if count % 500000 == 0:
            break

    with open(symspell_dic_paths, 'w', encoding='utf-8') as f:

        list1 = sorted(order_n_gram_dict.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1:
             f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, symspell_dic_paths))

    
def get_pattern_dict():
    '''
    @description:  得到pattern分词结果,没有停用词典
    @param {type} 
    @return:
    '''

    #order_n_gram_dict = {}
    
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    output_path = "/home/zixiang/Projects/text_correction/codebase/data"
    
    raw_train_paths = os.path.join(base_path,"xiaoai_v2.txt")
    symspell_dic_paths = os.path.join(output_path, "pattern_dict_3gram.txt")

    count = 0
    for sentence in open(raw_train_paths,'r'):
      
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        sentence = [i for i in sentence]
        length = len(sentence)

        for i in range(length):
            for j in range(i + 1,length):
                tmp_string  = sentence[i] + sentence[j]
                if tmp_string not in order_n_gram_dict:
                    order_n_gram_dict[tmp_string] = 1
                else:
                    order_n_gram_dict[tmp_string] += 1
                for k in range(j + 1,length):
                    tmp_string  = sentence[i] + sentence[j] + sentence[k]
                    if tmp_string not in order_n_gram_dict:
                        order_n_gram_dict[tmp_string] = 1
                        
                    else:
                        order_n_gram_dict[tmp_string] += 1

        if count % 10000 == 0:
            print("count {}".format(count))
            #print("order_n_gram_dict",order_n_gram_dict)
            print("dict len {}".format(len(order_n_gram_dict)))
        count += 1 

        if count % 2000000 == 0:
            break

    with open(symspell_dic_paths, 'w', encoding='utf-8') as f:
        list1 = sorted(order_n_gram_dict.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1:
             f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, symspell_dic_paths))

def get_ngram(arr,idx,res,k):
    if idx >= len(arr) :
        if len(res) == 1 :
                return
        if res not in order_n_gram_dict:
            order_n_gram_dict[res] = 1
        else:
            order_n_gram_dict[res] += 1
        return  
    if k == 0:
        if len(res) == 1 :
            return
        if res not in order_n_gram_dict:
            order_n_gram_dict[res] = 1
        else:
            order_n_gram_dict[res] += 1
        return 
    
    get_ngram(arr,idx+1,res+arr[idx],k-1)
    get_ngram(arr,idx+1,res,k)

if __name__ == "__main__":
    # print(get_order_n_gram(["你","是","谁","的","崽"]))
    # get_ngram(["你","是","谁","的","崽"],0,"",3)
    # print(ngram_list)
    get_pattern_dict_fixed(ngram=4)
    #get_pattern_dict()