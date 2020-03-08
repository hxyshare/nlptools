'''
@Author: your name
@Date: 2020-02-17 09:52:26
@LastEditTime: 2020-02-21 14:33:10
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /text_correction/codebase/utils/io_utils.py
'''
# -*- coding: utf-8 -*-
import os
import pickle
import json

def save_json(dict_to_save,path_to_save):
    '''
    @description:  save dict to txt file
    @param {type} 
    @return: 
    '''        
    fileObject = open(path_to_save, 'w')
    fileObject.write(json.dumps(dict_to_save))

def load_json(file_path):
    '''
    @description: 
    @param {type} 
    @return: 
    '''   
    load_f = open(file_path,'r')
    return json.load(load_f)
    
def load_pkl(pkl_path):
    """
    加载词典文件
    :param pkl_path:
    :return:
    """
    with open(pkl_path, 'rb') as f:
        result = pickle.load(f)
    return result


def dump_pkl(vocab, pkl_path, overwrite=True):
    """
    存储文件
    :param pkl_path:
    :param overwrite:
    :return:
    """
    if os.path.exists(pkl_path) and not overwrite:
        return
    with open(pkl_path, 'wb') as f:
        # pickle.dump(vocab, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(vocab, f, protocol=0)
