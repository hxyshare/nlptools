import re

re_han = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._]+)", re.U)

print(re_han.match("扶老奶奶过吗路阿斯顿方式方法但是是"))
print(re_han.split("扶老奶奶过吗路阿斯顿方式方0法但是是"))