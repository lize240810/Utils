# -*- coding: utf-8 -*-
'''
PV（Page View）访问量：
即页面浏览量或点击量，衡量网站用户访问的网页数量；在一定统计周期内用户每打开或刷新一个页面就记录1次，多次打开或刷新同一页面则浏览量累计。

UV（Unique Visitor）独立访客：
统计1天内访问某站点的用户数(以cookie为依据);访问网站的一台电脑客户端为一个访客。可以理解成访问某网站的电脑的数量。网站判断来访电脑的身份是通过来访电脑的cookies实现的。如果更换了IP后但不清除cookies，再访问相同网站，该网站的统计中UV数是不变的。如果用户不保存cookies访问、清除了cookies或者更换设备访问，计数会加1。00:00-24:00内相同的客户端多次访问只计为1个访客。

IP（Internet Protocol）独立IP数：
是指1天内多少个独立的IP浏览了页面，即统计不同的IP浏览用户数量。同一IP不管访问了几个页面，独立IP数均为1；不同的IP浏览页面，计数会加1。 IP是基于用户广域网IP地址来区分不同的访问者的，所以，多个用户（多个局域网IP）在同一个路由器（同一个广域网IP）内上网，可能被记录为一个独立IP访问者。如果用户不断更换IP，则有可能被多次统计。

会话次数（网站访问量）Session：
会话是指在指定的时间段内在您的网站上发生的一系列互动，所以会话次数是一段时间内用户向您的网站发起的会话（Session）总数量。一次会话会浏览一个或多个页面
'''
# #######################
'''
站点（流量）统计
    业务、术语
    独立服务（b[js]/s[flask]）
        次数：
            PV: 用户每打开或刷新一个页面就记录1次
            UV: 以cookie为依据(某一个值，不同值的个数)
            IP: 访客IP
        端：
            User-Agent: 浏览器标识
        SEO:
           Referer： 来路（从哪儿来）
        业务：
            URL: 路由
        时间
        -------------------------------------------
        分析
        可视化
'''
import uuid
from datetime import datetime, timedelta

from flask import Flask, make_response, request, abort

from dbhelper import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '!secret!'
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Record(db.Model):
    __tablename__ = 'records'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    uid = db.Column(db.Text, nullable=True, comment='独立访客ID')
    is_regular = db.Column(db.Boolean, default=False, comment='是否是回头客访问')
    referer = db.Column(db.Text, nullable=True, comment='从哪个URL来')
    accept_language = db.Column(db.Text, nullable=True, comment='Accept-Language头')
    user_agent = db.Column(db.Text, nullable=True, comment='User-Agent头')
    x_real_ip = db.Column(db.Text, nullable=True, comment='代理传递的真实IP')
    x_forwarded_for = db.Column(db.Text, nullable=True, comment='代理传递的真实域名')
    real_ip = db.Column(db.Text, nullable=True, comment='预处理后的真实IP')
    host = db.Column(db.Text, nullable=True, comment='Host头')
    url = db.Column(db.Text, nullable=True, comment='访问的URL')
    dt_str = db.Column(db.Text, nullable=True, comment='日期时间字符串(程序)')
    visit_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), comment='日期时间(数据库库)')
    

    def __repr__(self):
        return '<Record(_id={0})>'.format(self._id)

    def to_dict(self):
        return {
            '_id': self._id,
            'uid': self.uid,
            'is_regular': self.is_regular,
            'referer': self.referer,
            'accept_language': self.accept_language,
            'user_agent': self.user_agent,
            'x_real_ip': self.x_real_ip,
            'x_forwarded_for': self.x_forwarded_for,
            'real_ip': self.real_ip,
            'host': self.host,
            'url': self.url,
            'dt_str': self.dt_str,
            'visit_time': self.visit_time
        }

def build_response(url):
    # 构造响应
    resp = make_response('', 204)
    # 设置MimeType是CSS(欺骗浏览器)
    resp.headers['Content-Type'] = 'text/css'
    # 获取cookie（辨别: 回头客、独立访客）
    _uid = request.cookies.get('uid')
    dt_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    is_regular = True # 是否是回头客
    if not _uid:
        is_regular = False
        _uid = uuid.uuid5(uuid.NAMESPACE_DNS, dt_str).hex
        # refer: https://stackoverflow.com/questions/26613435/python-flask-not-creating-cookie-when-setting-expiration/26613642#26613642
        # refer: https://stackoverflow.com/questions/46661083/how-to-set-cookie-in-python-flask/46664792#46664792
        expire_date = datetime.now()
        expire_date = expire_date + timedelta(days=30)
        resp.set_cookie('uid', _uid, expires=expire_date)

    # 作记录
    func_record(url, _uid, is_regular, dt_str)

    return resp

def func_record(url, uid, is_regular, dt_str):
    '''存储记录（到数据库、文件等）'''
    referer = request.headers.get('Referer', None) # 从哪儿来
    accept_language = request.headers.get('Accept-Language', None) # 客户端语言
    user_agent = request.headers.get('User-Agent', None) # 客户端标识
    x_real_ip = request.headers.get('X-Real-Ip', None) # 代理真实IP
    x_forwarded_for = request.headers.get('X-Forwarded-For', None) # 代理前置IP
    real_ip = client_ip() # 客户端真实IP（而不是代理IP）
    host = request.host # 客户端访问地址（域名）

    # 存储记录
    record = Record()
    record.uid = uid
    record.is_regular = is_regular
    record.dt_str = dt_str
    record.referer = referer
    record.accept_language = accept_language
    record.user_agent = user_agent
    record.x_real_ip = x_real_ip
    record.x_forwarded_for = x_forwarded_for
    record.real_ip = real_ip
    record.host = host
    record.url = url
    # 提交
    db.session.add(record)
    db.session.commit()

    from pprint import pprint
    pprint(record.to_dict())

def client_ip():
    '''获取客户端真实IP'''
    real_ip = request.headers.get('X-Forwarded-For')
    if not bool(real_ip):
        # 没有代理，说明是开发环境
        real_ip = request.remote_addr

    return real_ip

@app.route('/')
def view_func():
    # 访问的请求的页面中的URL
    url = request.values.get('url')
    if not bool(url):
        return abort(400)
    resp = build_response(url)

    return resp

# 创建数据库
with app.test_request_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)