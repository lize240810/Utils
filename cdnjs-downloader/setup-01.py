# -*- coding: utf-8 -*-
import json

import requests

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit import print_formatted_text


kw = input('library keyword: ')
resp = requests.get('https://api.cdnjs.com/libraries?search={0}'.format(kw))
if resp.ok:
    data = json.loads(resp.text)
    if isinstance(data, dict) and 'results' in data:
        results = data['results']
        results = sorted(list(map(lambda item: item['name'], results)), reverse=False)

        completer = WordCompleter(results, ignore_case=True, match_middle=True)
        selected = prompt('choose library: ', completer=completer, complete_while_typing=True)
        if selected in results:
            print('your choice is:', end=' ')
            print_formatted_text(ANSI('\x1b[91m{0}'.format(selected)))
        else:
            print('canceled')