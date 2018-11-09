# -*- coding: utf-8 -*-
import json

import requests

from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit import print_formatted_text

# tip: [new_radio_list.py] file is in gist(https://gist.github.com/gsw945/3f41738e9641a330c64bf2f5a9a97fdf)
from new_radio_list import NewRadioList


library = 'jqueryui'
resp = requests.get('https://api.cdnjs.com/libraries/{0}?fields=assets'.format(library))
if resp.ok:
    data = json.loads(resp.text)
    if isinstance(data, dict) and 'assets' in data:
        assets = data['assets']
        versions = list(map(lambda item: item['version'], assets))
        print(versions)
        values = list(map(lambda item: (item, item), versions))
        rdo = NewRadioList(values)

        def do_exit(event):
            # get_app().exit()
            event.app.exit(result=rdo.current_value)
        def do_up_down(event):
            print(event)
            pass
        bindings = KeyBindings()
        bindings.add('enter')(do_exit)
        app_bindings = merge_key_bindings([
            load_key_bindings(),
            bindings
        ])

        selected = Application(layout=Layout(rdo), key_bindings=app_bindings).run()
        print('your choice is:', end=' ')
        # refer: https://github.com/jonathanslenders/python-prompt-toolkit/blob/master/examples/print-text/ansi.py
        print_formatted_text(ANSI('\x1b[91m{0}'.format(selected)))