# -*- coding: utf-8 -*-
import os
import json

import requests


# root_folder = os.path.dirname(__file__)
root_folder = os.getcwd()

library = 'jqueryui'
resp = requests.get('https://api.cdnjs.com/libraries/{0}?fields=assets'.format(library))
if resp.ok:
    data = json.loads(resp.text)
    if isinstance(data, dict) and 'assets' in data:
        assets = data['assets']
        version = '1.12.1'
        selected = list(filter(lambda item: item['version'] == version, assets))
        files = selected[0]['files']
        # begin to download
        folder = os.path.join(root_folder, library, version)
        # if not os.path.exists(folder) or not os.path.isdir(folder):
        #     os.makedirs(folder)
        print('store to [{0}]'.format(folder))
        base_url = 'https://cdnjs.cloudflare.com/ajax/libs/{0}/{1}/'.format(library, version)
        list_len = len(files)
        for idx, item in enumerate(files):
            url = base_url + item
            # from: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html#id4
            resp = requests.get(url)
            if resp.ok:
                item_path = item.replace('/', os.sep)
                full_path = os.path.join(folder, item_path)
                file_folder = os.path.dirname(full_path)
                if not os.path.exists(file_folder) or not os.path.isdir(file_folder):
                    os.makedirs(file_folder)
                with open(full_path, 'wb') as fw:
                    fw.write(resp.content)
                print('{0:2}/{1:2}'.format(idx + 1, list_len), end=' -> ')
                print(item)
            else:
                print(resp.status_code, end=' -> ')
                print(url)