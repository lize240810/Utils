# -*- coding: utf-8 -*-
# need to upgrade the default Python version on Ubuntu 16.04
# refer:
#   https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get
#   https://aiohttp.readthedocs.io/en/stable/web_advanced.html#static-file-handling
import os
import logging

try:
    from aiohttp import web
except ImportError:
    os.system('pip install aiohttp')
    from aiohttp import web


# 启用日志
logging.basicConfig(level=logging.DEBUG)
# 当前目录
CWD = os.path.dirname(os.path.abspath(__file__))

@web.middleware
async def mw_index(request, handler):
    '''中间件[将index.html作为默认文件]'''
    global CWD
    # 如果访问的是目录
    path = request.path[1:(-1 if request.path.endswith('/') else None):]
    lp = path.replace('/', os.sep)
    idxd = os.path.join(CWD, lp)
    if os.path.exists(idxd) and os.path.isdir(idxd):
        idxdf = os.path.join(idxd, 'index.html')
        if os.path.exists(idxdf):
            idxu = '/' + path + ('/' if len(path) > 0 else '') + 'index.html'
            return web.HTTPFound(idxu)
    resp = await handler(request)
    return resp

app = web.Application(middlewares=[mw_index])

static_route = web.static(
    '/',
    CWD,
    show_index=True)
app.add_routes([static_route])

if __name__ == '__main__':
    run_cfg = {
        'host': '0.0.0.0',
        'port': 9876
    }
    web.run_app(app, **run_cfg)
