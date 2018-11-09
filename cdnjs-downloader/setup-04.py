# -*- coding: utf-8 -*-
import os
import time
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Manager, freeze_support

import requests


def do_request(args):
    root_folder = os.getcwd()
    (library, version, url, share, data_len) = args
    folder = os.path.join(root_folder, library, version)
    base_url = 'https://cdnjs.cloudflare.com/ajax/libs/{0}/{1}/'.format(library, version)
    item_url = base_url + url
    # from: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html#id4
    resp = requests.get(item_url)
    if resp.ok:
        item_path = url.replace('/', os.sep)
        full_path = os.path.join(folder, item_path)
        file_folder = os.path.dirname(full_path)
        if not os.path.exists(file_folder) or not os.path.isdir(file_folder):
            os.makedirs(file_folder)
        with open(full_path, 'wb') as fw:
            fw.write(resp.content)
        share[url] = True
    else:
        print(resp.status_code, end=' -> ')
        print(item_url)
        share[url] = False
    time.sleep(0.2)
    # print(share)
    print('{0:2}/{1:2}'.format(len(share), data_len), end=' -> ')
    print(url)


if __name__ == '__main__':
    freeze_support()

    manager = Manager()
    share = manager.dict()
    N = 3
    tpool = ThreadPool(N)
    library = 'iframe-resizer'
    version = '3.6.2'
    data = [
        'ie8.polyfils.map',
        'ie8.polyfils.min.js',
        'iframeResizer.contentWindow.js',
        'iframeResizer.contentWindow.map',
        'iframeResizer.contentWindow.min.js',
        'iframeResizer.js',
        'iframeResizer.map',
        'iframeResizer.min.js'
    ]
    data_len = len(data)
    data = list(map(lambda item: (library, version, item, share, data_len), data))
    tresult_proxy = tpool.map_async(do_request, data)
    tpool.close()
    tpool.join()
    # result = tresult_proxy.get()