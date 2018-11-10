import requests
data = {
    'key' : 'f340271d9c23b28832e629ca1535f2b0',
    'city': 500106,
    'extensions':'base',
    # 'extensions':'all',
    'output' : 'JSON'
}

req = '''
    https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={key}&extensions={extensions}&output={output}
'''.format(**data)

# 获取全部信息
datas = requests.get(req).json()
# 获取第内容信息
lives = datas.pop('lives')[0]
# 获取头信息
head = '''
返回状态:{status}
返回结果总数目:{count}
返回的状态信息:{info}
返回状态说明,10000代表正确:{infocode}
'''.format(**datas)

content = '''
省份名:{province}
城市名:{city}
区域编码:{adcode}
天气现象（汉字描述）:{weather}
实时气温，单位：摄氏度:{temperature}
风向描述:{winddirection}
风力级别，单位：级:{windpower}
空气湿度:{humidity}
数据发布的时间:{reporttime}
'''.format(**lives)