# -*- coding: utf-8 -*-
import sys
from codecs import open
import os
from sklearn.model_selection import train_test_split
import pandas as pd
from tokenizer import segment

def segment_sentence(data):
    source = []
    for line in data:
        source.append(segment(line.strip(), cut_type='char'))
    return source

def _save_data(file_path, data_path):
    with open(data_path, 'w', encoding='utf-8') as f:
        count = 0
        tmp_res = []
        for src in open(file_path,"r"):
            tmp_res.append([i for i in src.strip().split("\t")[1]])
            count += 1
            if count % 10000 == 0:
                for i in tmp_res:
                    f.write(' '.join(i) + '\n')
                tmp_res = []
                print("count {}".format(count))

        print("save line size:%d to %s" % (count, data_path))

def save_corpus_data(data_list, train_data_path, test_data_path):
    train_lst, test_lst = train_test_split(data_list, test_size=0.1)
    _save_data(train_lst, train_data_path)
    _save_data(test_lst, test_data_path)

def get_session_data(file_path, data_path):
    with open(data_path, 'w', encoding='utf-8') as f:
        count = 0
        tmp_res = []
        for src in open(file_path,"r"):
            tmp_res.append(src.strip().split("\t")[1])
            count += 1
            if count % 10000 == 0:
                for i in tmp_res:
                    f.write(''.join(i) + '\n')
                tmp_res = []
                print("count {}".format(count))

        print("save line size:%d to %s" % (count, data_path))


if __name__ == '__main__':
    # train data
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    data_list = []
    raw_train_paths = os.path.join(base_path,"xiaoai_v2.txt")
    new_raw_train_data_path = os.path.join(base_path,"domain_session_pairs.txt")
    train_data_path = os.path.join(base_path,"train_session_pairs.txt")
    train_session_path = os.path.join(base_path,"new_domain_session_pairs.txt")
    _save_data(new_raw_train_data_path,train_data_path)
    #get_session_data(new_raw_train_data_path,train_session_path)

    #old data luxiao 2000w
    #test_data_path = os.path.join(base_path, "test_query.txt")
    #train_data_path = os.path.join(base_path,"train_query.txt")
    #_save_data(raw_train_paths,train_data_path)
