# -*- coding: utf-8 -*-
'''
说明：
对称加密(明文 <==(key)==> 密文)

安装：
pip install cryptography

参考：
https://cryptography.io/en/latest/installation/
https://pythonguidecn.readthedocs.io/zh/latest/scenarios/crypto.html
https://zhuanlan.zhihu.com/p/25278582
'''
from cryptography.fernet import Fernet


# 生成秘钥（bytes）
key = Fernet.generate_key()
# 秘钥类型转文本（bytes->str，一般存储到配置文件）
key_str = key.decode('ascii', 'ignore')

# 文本秘钥转bytes(一般是从配置文件读取，为实例化密码器做准备)
key = key_str.encode('ascii', 'ignore')
# 实例化密码组（密码器）
cipher_suite = Fernet(key)
# --------------------------------------------------------------
# 原始数据(str)
raw_data = '这里是原始数据, Life is short, use Python. 1989,1991'
# 原始数据类型转成bytes，为加密作准备
data = raw_data.encode('utf-8', 'ignore')

# 加密（得到密文，bytes）
cipher_text = cipher_suite.encrypt(data)
# 将密文类型转成str（一般用于网络传输）
cipher_text_str = cipher_text.decode('ascii', 'ignore')
# --------------------------------------------------------------
# 密码从文本转成bytes，为解密做准备
cipher_text = cipher_text_str.encode('ascii', 'ignore')
# 解密（得到明文，bytes）

plain_text = cipher_suite.decrypt(cipher_text)
# 将明文类型转为str（一般用于页面显示、数据库查询参数等）
plain_text_str = plain_text.decode('utf-8', 'ignore')