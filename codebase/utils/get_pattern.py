# -*- coding: utf-8 -*-

from tokenizer import Tokenizer
from pyhanlp import *
from prefix_tree import Trie
import codecs

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

def get_ngram_pattern_fix(file_path,origin_file_path,output_pattern_dict_path):
    """修正得到ngram结果的pattern
    """
    word_list = set()
    order_n_gram_dict = {}
    replace_char = "*"
    count = 0
    #load dict 
    for i in open(file_path):
        word_list.add(i.strip().split("\t")[0])
        count += 1
        if count == 1000:
            break
    #print(word_list)
    count = 0
    for sentence in open(origin_file_path,'r'):
        count += 1
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        sentence = [i for i in sentence]
        length = len(sentence)
        tmp_res_set = set()
        for i in range(length):
            for j in range(i + 1,length):
                tmp_string  = sentence[i] + sentence[j]
                tmp_res_set.add(tmp_string)

        intersection = tmp_res_set.intersection(word_list)

        for i in intersection:
            
            tmp_i = [k for k in i]
            tmp_sentence = sentence
            for j in range(length):
                if tmp_sentence[j] not in tmp_i:
                    tmp_sentence[j] = replace_char

            tmp_string = ""
            add_flag = True
            for j in tmp_sentence:
                
                if j == "*" :
                    if add_flag:
                        tmp_string = tmp_string + replace_char
                        add_flag = False
                else:
                    tmp_string = tmp_string + j
                    add_flag = True

            if tmp_string == "*":   
                continue
                    
            if tmp_string not in order_n_gram_dict:
                order_n_gram_dict[tmp_string] = 1
            else:
                order_n_gram_dict[tmp_string] += 1
        
        if count % 10000 == 0:
            print(" count {}".format(count))
            
        #print(intersection)
        #print(sentence)

    with open(output_pattern_dict_path, 'w', encoding='utf-8') as f:
        list1 = sorted(order_n_gram_dict.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1[:6000]:
                f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, output_pattern_dict_path))

def get_pattern_dict(raw_train_paths,symspell_dic_paths):
    '''
    @description:  得到pattern dict 分词结果,和 NER 结果没有停用词典
    保留停用词典
    @param {type} 
    @return:
    '''
    
    jieba_tokenizer = Tokenizer()
    tokenizer = HanLP.newSegment().enableOrganizationRecognize(True)
    dict_fenci = {}

    count = 0
    for sentence in open(raw_train_paths,'r'):
    
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        #分词
        for j in [i[0] for i in jieba_tokenizer.tokenize(sentence)]:
            #if j not in stop_words and len(j) >= 2 :
                if j not in dict_fenci:
                    dict_fenci[j] = 1
                else:
                    dict_fenci[j] += 1
        
        if count % 10000 == 0:
            print("count {}".format(count))
            print("dict len {}".format(len(dict_fenci)))
        count += 1 
        if count % 3000000 == 0:
            break
    #ner
    count = 0
    for sentence in open(raw_train_paths,'r'):      
    
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        for j in [str(i.word) for i in tokenizer.seg(sentence)]:
                if j not in dict_fenci :
                    dict_fenci[j] = 1
                else:
                    dict_fenci[j] += 1

        if count % 10000 == 0:
            print("count {}".format(count))
            print("dict len {}".format(len(dict_fenci)))
        count += 1 
        if count % 3000000 == 0:
            break

    with open(symspell_dic_paths, 'w', encoding='utf-8') as f:
        count = 0
        list1 = sorted(dict_fenci.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1:
             f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, symspell_dic_paths))

def get_ngram_pattern(file_path,origin_file_path,output_pattern_dict_path):
    """得到ngram结果的pattern
    """
    word_list = set()
    order_n_gram_dict = {}
    replace_char = "*"
    count = 0
    #load dict 
    for i in open(file_path):
        word_list.add(i.strip().split("\t")[0])
        count += 1
        if count == 30000:
            break
    #print(word_list)
    count = 0
    for sentence in open(origin_file_path,'r'):
        count += 1
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue

        sentence = [i for i in sentence]
        length = len(sentence)
        tmp_res_set = set()
        for i in range(length):
            for j in range(i + 1,length):
                tmp_string  = sentence[i] + sentence[j]
                tmp_res_set.add(tmp_string)

                for k in range(j + 1,length):
                    tmp_string  = sentence[i] + sentence[j] + sentence[k]
                    tmp_res_set.add(tmp_string)
                    for t in range(k + 1,length):
                        tmp_string  = sentence[i] + sentence[j] + sentence[k] + sentence[t]
                        tmp_res_set.add(tmp_string)


        intersection = tmp_res_set.intersection(word_list)

        for i in intersection:
            
            tmp_i = [k for k in i]
            tmp_sentence = sentence
            for j in range(length):
                if tmp_sentence[j] not in tmp_i:
                    tmp_sentence[j] = replace_char

            tmp_string = ""
            add_flag = True
            for j in tmp_sentence:
                
                if j == "*" :
                    if add_flag:
                        tmp_string = tmp_string + replace_char
                        add_flag = False
                else:
                    tmp_string = tmp_string + j
                    add_flag = True

            if tmp_string == "*":   
                continue
                    
            if tmp_string not in order_n_gram_dict:
                order_n_gram_dict[tmp_string] = 1
            else:
                order_n_gram_dict[tmp_string] += 1
        
        if count % 10000 == 0:
            print(" count {}".format(count))
        if count % 200000 == 0:
            break

        #print(intersection)
        #print(sentence)

    with open(output_pattern_dict_path, 'w', encoding='utf-8') as f:
        list1 = sorted(order_n_gram_dict.items(),key=lambda item:item[1],reverse=True)

        for key,value in list1[:6000]:
                f.write(key + '\t'+ str(value) +'\n')

        print("save line size:%d to %s" % (count, output_pattern_dict_path))
    
def get_replace_pattern(file_path,origin_file_path,jieba_tokenizer,output_pattern_dict_path):
    """对NER和分词结果保留高频词
    """
    word_list = []
    dict_pattern = {}
    replace_char = "*"
    count = 0
    tokenizer = HanLP.newSegment().enableOrganizationRecognize(True)
    for i in open(file_path):
        word_list.append(i.strip().split("\t")[0])
        count += 1
        if count == 100:
            break
    
    count = 0 
    for sentence in open(origin_file_path,'r'):
        count += 1
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue
        
        #print([i[0] for i in jieba_tokenizer.tokenize(sentence)])
        tmp_string = ""
        add_flag = True
        #for j in [str(i.word) for i in tokenizer.seg(sentence)]:
        for j in [i[0] for i in jieba_tokenizer.tokenize(sentence)]:
            if j not in word_list :
                if add_flag:
                    tmp_string = tmp_string + replace_char
                    add_flag = False
            else:
                tmp_string = tmp_string + j
                add_flag = True

        if tmp_string not in dict_pattern:
            dict_pattern[tmp_string] = 1
        else:
            dict_pattern[tmp_string] += 1
        
        if count % 10000 == 0:
            print("tmp_string {} count {}".format(tmp_string,count))
        if count % 8000000 == 0:
            break

    with open(output_pattern_dict_path, 'w', encoding='utf-8') as f:

        list1 = sorted(dict_pattern.items(),key=lambda item:item[1],reverse=True)
        tmp_value = 0
        for key,value in list1:
                f.write(key + '\t'+ str(value) + '\t' + ('{:.2%}'.format((value+tmp_value)/8000000)) + '\n')
                tmp_value += value

        print("save line size:%d to %s" % (count, output_pattern_dict_path))

    
def get_replace_pattern2(file_path,origin_file_path,jieba_tokenizer,output_pattern_dict_path):
    """去除高频不重要的词
    """
    word_list = []
    dict_pattern = {}
    replace_char = "*"
    count = 0
    for i in open(file_path):

        word_list.append(i.strip().split("\t")[0])
        count += 1
    
        if count == 5000:
            break
    
    count = 0 
    for sentence in open(origin_file_path,'r'):
        count += 1
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue
        
        #print([i[0] for i in jieba_tokenizer.tokenize(sentence)])
        tmp_string = ""
        add_flag = True
        for j in [i[0] for i in jieba_tokenizer.tokenize(sentence)]:
            
            if j in word_list :
                if add_flag:
                    tmp_string = tmp_string + replace_char
                    add_flag = False
            else:
                tmp_string = tmp_string + j
                add_flag = True

        if tmp_string not in dict_pattern:
            dict_pattern[tmp_string] = 1
        else:
            dict_pattern[tmp_string] += 1
        
        if count % 10000 == 0:
            print("tmp_string {} count {}".format(tmp_string,count))
        if count % 8000000 == 0:
            break


    with open(output_pattern_dict_path, 'w', encoding='utf-8') as f:
        list1 = sorted(dict_pattern.items(),key=lambda item:item[1],reverse=True)
        tmp_value = 0
        for key,value in list1:
                f.write(key + '\t'+ str(value) + '\t' + ('{:.2%}'.format((value+tmp_value)/8000000)) + '\n')
                tmp_value += value

        print("save line size:%d to %s" % (count, output_pattern_dict_path))

odef add_result(input_file_list ,output_pattern_dict_path):
    """把多个结果融合在一起
    """
    pattern_dict = {}
    count = 0
    for f in input_file_list:
        for line in open(f):
            pattern, nu , _ = line.strip().split("\t")
            if len(pattern) < 3 :
                continue

            count += 1
            nu = int(nu)
            if pattern not in pattern_dict:
                pattern_dict[pattern]  = nu
            else:
                pattern_dict[pattern] += nu

            if count % 1000 == 0:
                print("count",count)
            
            if count % 5000 == 0:
                break
 
    #print(pattern_dict)
    with open(output_pattern_dict_path, 'w', encoding='utf-8') as f:

        list1 = sorted(pattern_dict.items(),key=lambda item:item[1],reverse=True)
        tmp_value = 0
        for key,value in list1:
                f.write(key + '\t'+ str(value//2) + '\t' + ('{:.2%}'.format((value+tmp_value)/16000000)) + '\n')
                tmp_value += value

        print("save line size:%d to %s" % (count, output_pattern_dict_path))


def get_ner(input_file,input_pattern,output_ner_dict_path):
    
    trie = Trie()
    ner_dict = {}
    count = 0
    for line in open(input_pattern):
        tmp_pattern = [i for i in line.strip().split("\t")[0]]
        
        if len(tmp_pattern) < 2:
            print(tmp_pattern)
            continue

        trie.insert(tmp_pattern)
        count += 1
        if count == 50:
            break

    count = 0
    for line in open(input_file):
        isword,word_path,pattern= trie.search([i for i in line.strip()])
        pattern_list = [i for i in pattern.split("*") if i ]
        word_list = [i for i in word_path.split("*") if i ]
        #print(word_list)
        if len(pattern_list) == 1 and len(pattern_list[0]) == 1:
            #print(pattern)
            continue
        if not isword and len(word_path) ==  0:
            continue
        else:
            if len(word_list) == 0:
                continue
            
            elif len(word_list) == 1:
                if len(word_list[0]) == 1:
                    continue
                if word_list[0] in ner_dict:
                    ner_dict[word_list[0]] += 1
                else:
                    ner_dict[word_list[0]] = 1
            # elif len(word_list) > 1 :

            #     if word_list[-1] in ner_dict:
            #         ner_dict[word_list[-1]] += 1
            #     else:
            #         ner_dict[word_list[-1]] = 1

            count += 1

        if count % 10000 == 0:
            print(count)
            print("word:",word_path,"<---->","pattern:",pattern,isword)
        # if "你给我" in pattern:
        #     print("word:",word_path,"<---->","pattern:",pattern,isword)
    with open(output_ner_dict_path, 'w', encoding='utf-8') as f:

        list1 = sorted(ner_dict.items(),key=lambda item:item[1],reverse=True)
        tmp_value = 0
        for key,value in list1:
                f.write(key + '\t'+ str(value//2) + '\n')
                tmp_value += value

        print("save line size:%d to %s" % (count, output_ner_dict_path))

def gen_pattern2():
   """
   得到去除高频不重要的词的pattern
   """
   input_origin_file = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog/xiaoai_v2.txt"
   input_dict = "/home/zixiang/Projects/text_correction/codebase/data/gen_pattern_dict.txt"
   output_pattern_dict_path = "/home/zixiang/Projects/text_correction/codebase/data/pattern_rm.txt"
   jieba_tokenizer  = Tokenizer()
   get_replace_pattern2(input_dict,input_origin_file,jieba_tokenizer,output_pattern_dict_path)


def gen_pattern3():
    """
    得到对NER和分词结果保留高频词pattern
    """
    #old data
    # input_origin_file = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog/xiaoai_v2.txt"
    # input_dict = "/home/zixiang/Projects/text_correction/codebase/data/pattern_origin_dict.txt"
    # output_pattern_dict_path = "/home/zixiang/Projects/text_correction/codebase/data/pattern_ner.txt"
    
    input_origin_file = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog/new_domain_session_pairs.txt"
    input_dict = "/home/zixiang/Projects/text_correction/codebase/data/new_domain_session_pairs_dict.txt"
    output_pattern_dict_path = "/home/zixiang/Projects/text_correction/codebase/data/new_domain_session_pairs_pattern.txt"
    jieba_tokenizer  = Tokenizer()
    get_replace_pattern(input_dict,input_origin_file,jieba_tokenizer,output_pattern_dict_path)

def load_word_freq_dict(path):
        """
        加载切词词典
        :param path:
        :return:
        """
        word_freq = {}
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    continue
                info = line.split('\t')
                if len(info) < 1:
                    continue
                word = info[0]
                # 取词频，默认1
                freq = int(info[1]) if len(info) > 1 else 1
                word_freq[word] = freq
        return word_freq

def gen_pattern_ngram():
    """ 得到ngram结果的pattern
    """
    input_origin_file = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog/xiaoai_v2.txt"
    input_dict = "/home/zixiang/Projects/text_correction/codebase/data/pattern_dict_4gram_fixed.txt"
    output_pattern_dict_path = "/home/zixiang/Projects/text_correction/codebase/data/pattern_ngram.txt"
    
    get_ngram_pattern(input_dict,input_origin_file,output_pattern_dict_path)


def get_pattern_pipeline():
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    output_path = "/home/zixiang/Projects/text_correction/codebase/data"

    input_file = os.path.join(base_path,"new_domain_session_pairs.txt")
    output_file = os.path.join(output_path, "new_domain_session_pairs_dict.txt")
    output_pattern_dict_path = "/home/zixiang/Projects/text_correction/codebase/data/new_domain_session_pairs_pattern.txt"
    jieba_tokenizer  = Tokenizer()
    get_pattern_dict(input_file,output_file)
    get_replace_pattern(output_file,input_file,jieba_tokenizer,output_pattern_dict_path)

def get_ner_pipeline():
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    output_path = "/home/zixiang/Projects/text_correction/codebase/data"

    input_file = os.path.join(base_path,"new_domain_session_pairs.txt")
    output_file = os.path.join(output_path, "new_domain_session_pairs_dict.txt")
    output_pattern_dict_path = "/home/zixiang/Projects/text_correction/codebase/data/new_domain_session_pairs_pattern.txt"
    jieba_tokenizer  = Tokenizer()
    output_ner_dict_path = os.path.join(output_path, "new_domain_session_pairs_ner.txt")
    #get_pattern_dict(input_file,output_file)
    #get_replace_pattern(output_file,input_file,jieba_tokenizer,output_pattern_dict_path)
    get_ner(input_file,output_pattern_dict_path,output_ner_dict_path)

def test_tokenize():
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"

    input_file = os.path.join(base_path,"new_domain_session_pairs.txt")
    output_path = "/home/zixiang/Projects/text_correction/codebase/data"
    output_ner_dict_path = os.path.join(output_path, "new_domain_session_pairs_ner.txt")
    custom_word_freq_path = os.path.join(output_path, 'data/custom_word_freq.txt')
    #search 把所有结果搜索出来,default 精确模式
    jieba_tokenizer  = Tokenizer(dict_path=custom_word_freq_path, custom_word_freq_dict=load_word_freq_dict(output_ner_dict_path))
    #jieba_tokenizer  = Tokenizer()
   
    for sentence in open(input_file,'r'):
        sentence = sentence.strip()
        if not is_chinese_string(sentence) :
            continue
        print(sentence)
        print([jieba_tokenizer.tokenize(sentence,mode='default')])

def update_pattern():
    new_pattern = "/home/zixiang/Projects/text_correction/codebase/data/new_domain_session_pairs_pattern.txt"
    origin_pattern = "/home/zixiang/Projects/text_correction/codebase/data/pattern.txt"
    file_list = [new_pattern,origin_pattern]
    add_result(file_list,origin_pattern)

if __name__ == "__main__":
    # input_pattern_path1 = "/home/zixiang/Projects/text_correction/codebase/data/pattern_fenci.txt"
    # input_pattern_path2 = "/home/zixiang/Projects/text_correction/codebase/data/pattern_ner.txt"
    # #input_pattern_path3 = "/home/zixiang/Projects/text_correction/codebase/data/pattern_rm.txt"
    # output_path = "/home/zixiang/Projects/text_correction/codebase/data/pattern.txt"
    # file_list = [input_pattern_path1,input_pattern_path2]
    # add_result(file_list,output_path)
    # get_ner_pipeline()
    # test_tokenize()
    update_pattern()