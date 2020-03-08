import pandas as pd
df = pd.read_excel("/home/zixiang/Downloads/2020Q1第7周0210-0214语音助手端到端标注分析.xlsx")
shibie = df[df["错误原因"] == "识别错误"]
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

import jieba
from pyhanlp import *
import hanlp
import jieba.posseg as pseg


# for i in  shibie["query"]:
#     if len(i) > 2 and is_chinese_string(i):
#         #seg_list = jieba.cut(i) 
#         seg_list = pseg.cut(i)
#         for word, flag in seg_list:
#             print('%s %s' % (word, flag))

# test_sentence = "如果想配音应该上什么大学"
tokenizer = HanLP.newSegment().enableOrganizationRecognize(True)
#tokenizer.enablePartOfSpeechTagging(False)

# print(tokenizer.seg(test_sentence))
# print(HanLP.parseDependency(test_sentence))
pos_count = 0
v_count = 0
rate_count1 = 0 
rate_count2 = 0
count = 0
rate_count3 = 0

for index, row in shibie.iterrows():
    i = row["query"]
    j = row["正确识别文本"]
    a = []
    b = []
    c = []
    d = []
    if len(i) > 2 and is_chinese_string(i):
        #seg_list = jieba.cut(i) 
        count += 1
        cuowu_list = tokenizer.seg(i)
        for term in cuowu_list:
            a.append(str(term.nature))
        correct_list = tokenizer.seg(j)
        for term in correct_list:
            b.append(str(term.nature))
        #print(type(cuowu_list),j,correct_list)
     
        # for i in a:
        #     if "v" == i:
        #         v_count += 1

        # if v_count > 2:
        #     count += 1

        if len(a) > len(b):
             pos_count += 1

        for word in HanLP.parseDependency(i).iterator():  
            c.append(word.DEPREL)

        for word in HanLP.parseDependency(j).iterator():  
            d.append(word.DEPREL)

        if len(c) > len(d):
            v_count += 1
        
        rate_count1 += len(i)/len(a)
        rate_count2 += len(j)/len(b)
        
        if len(j)/len(b) > 1.68 :
            print(len(j)/len(b))
            rate_count3 += 1
        print(i,a,c,len(i)/len(a),j,b,d,len(j)/len(b))
        

print(pos_count,v_count,rate_count1/count,rate_count2/count ,rate_count3,count)