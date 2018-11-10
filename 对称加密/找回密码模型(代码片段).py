import json
from datetime import datetime, timedelta


expires = 3600 * 24 * 3

# ---------------------------------------------------------------------------------

user_info = {
    'id': 1,
    'email': 'abc@qq.com',
    'send_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
data = json.dumps(user_info)
data_bytes = data.encode('utf-8', 'ignore')
# TODO：加密
# ---------------------------------------------------------------------------------
# TODO：解密
# 如果 解密成功，会得到 user_info
# 如果 解密失败，说明数据有误（不是我们给的）
send_datetime = datetime.strptime(user_info['send_datetime'], '%Y-%m-%d %H:%M:%S')
if datetime.now() - send_datetime <= timedelta(seconds=expires):
    # 有效
    print('有效')
    # TODO: 重置密码
    pass
else:
    # 过期了
    print('过期了')
    pass