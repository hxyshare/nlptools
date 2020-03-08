# -*- coding:utf-8 -*-

from pyhanlp import *
import hanlp

test_sentence = "如果想配音应该上什么大学"
tokenizer = HanLP.newSegment().enableOrganizationRecognize(True)

print(tokenizer.seg(test_sentence))
print(HanLP.parseDependency(test_sentence))
# recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
# # print(recognizer([list('上海华安工业（集团）公司董事长谭旭光和秘书张晚霞来到美国纽约现代艺术博物馆参观。'),
# #                 list('萨哈夫说，伊拉克将同联合国销毁伊拉克大规模杀伤性武器特别委员会继续保持合作。')]))

# #tokenizer = HanLP.newSegment().enableOrganizationRecognize(True)


# for sentence in open("/home/zixiang/DataSets/berttestdata/xiaoaiquerylog/new_domain_session_pairs.txt"):
#     print(sentence)
#     print([i[0] for i in recognizer(sentence)])