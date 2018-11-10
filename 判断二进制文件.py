from binaryornot.check import is_binary
import os
with open('jk.txt','wb+') as f:
    cc="第三方凉快凉快圣诞节饭".encode('utf-8')
    f.write(cc)
is_binary('jk.txt')