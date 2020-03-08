# coding=utf8
import re

def test_find_pattern():
    regex1 = r"怎么预防(.*)"
    regex2 = r"什么是(.*)"
    regex3 = r"(.*)怎么预防"

    test_str = ["怎么预防是的方式地方\n",
        "什么是是否是否地方是否\n",
        "山东省方法地方怎么预防"]

    for line in test_str:

        mysearch1 = re.search(regex1,line)
        mysearch2 = re.search(regex2,line)
        mysearch3 = re.search(regex3,line)

        if mysearch1:
            print("mysearch1",mysearch1.group(1))
        if mysearch2:
            print("mysearch2",mysearch2.group(1))
        if mysearch3:
            print("mysearch3",mysearch3.group(1))

def find_pattern(input_text):

    regex1 = r"怎么*样*预防 (.*)"
    regex2 = r"什么是(.*)"
    regex3 = r"(.*)怎么*样*预防"
    regex4 = r"(.*)是什么"
    regex5 = r"播放(.*)的*新闻"


    mysearch1 = re.search(regex1,input_text)
    mysearch2 = re.search(regex2,input_text)
    mysearch3 = re.search(regex3,input_text)
    mysearch4 = re.search(regex4,input_text)
    mysearch5 = re.search(regex5,input_text)

    if mysearch1:
        if len(mysearch1.group(1)) != 0:
            return mysearch1.group(1),1
    if mysearch2:
        if len(mysearch2.group(1)) != 0:
            return mysearch2.group(1),2
    if mysearch3:
        if len(mysearch3.group(1)) != 0:
            return mysearch3.group(1),3
    if mysearch4:
        if len(mysearch4.group(1)) != 0:
            return mysearch4.group(1),4
    if mysearch5:
        if len(mysearch5.group(1)) != 0:
            return mysearch5.group(1),5

if __name__ == "__main__":
    #print(find_pattern("播放是否方式地方新闻"))
    print(find_pattern("怎么样预防是否方式地方新闻"))