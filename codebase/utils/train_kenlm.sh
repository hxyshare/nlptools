/home/zixiang/ExtraData/kenlm/build/bin/lmplz -o 3 --verbose_header --text ~/DataSets/berttestdata/xiaoaiquerylog/train_query.txt --arpa ./xiaoai_query_correct_20200303.arpa
/home/zixiang/ExtraData/kenlm/build/bin/build_binary -s xiaoai_query_correct_20200303.arpa xiaoai_query_correct_20200303.bin
mv xiaoai_query_correct_20200303.bin /home/zixiang/.corrector/datasets
rm xiaoai_query_correct_20200303.arpa