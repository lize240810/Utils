# http://www.tuling123.com/
import requests

#改成你自己的图灵机器人的api
apiUrl = 'http://www.tuling123.com/openapi/api'
msg = '你好'
data = {
    'key': '769e14179d3844948f04364d92fbd14b',  # Tuling Key
    'info': msg,  # 这是我们发出去的消息
    'userid': 'wechat-robot',  # 这里你想改什么都可以
}
# 我们通过如下命令发送一个post请求
resp = requests.post(apiUrl, data=data).json()
reply = resp.get('text')
print(reply)