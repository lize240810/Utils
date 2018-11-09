# -*- coding: utf-8 -*-
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.formatted_text import HTML


class NewRadioList(object):
    """
    List of radio buttons. Only one can be checked at the same time.
    :param values: List of (value, label) tuples.

    modified from: https://github.com/jonathanslenders/python-prompt-toolkit/blob/master/prompt_toolkit/widgets/base.py
    """
    def __init__(self, values):
        assert isinstance(values, list)
        assert len(values) > 0
        assert all(isinstance(i, tuple) and len(i) == 2
                   for i in values)

        self.values = values
        self.current_value = values[0][0]
        self._selected_index = 0

        # Key bindings.
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            self._selected_index = max(0, self._selected_index - 1)
            self.current_value = self.values[self._selected_index][0]

        @kb.add('down')
        def _(event):
            self._selected_index = min(
                len(self.values) - 1,
                self._selected_index + 1
            )
            self.current_value = self.values[self._selected_index][0]

        @kb.add(Keys.Any)
        def _(event):
            # We first check values after the selected value, then all values.
            for value in self.values[self._selected_index + 1:] + self.values:
                if value[0].startswith(event.data):
                    self._selected_index = self.values.index(value)
                    return

        # Control and window.
        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=kb,
            focusable=True)

        self.window = Window(
            content=self.control,
            style='class:radio-list',
            right_margins=[
                ScrollbarMargin(display_arrows=True),
            ],
            dont_extend_height=True)

    def _get_text_fragments(self):
        result = []
        for i, value in enumerate(self.values):
            checked = (value[0] == self.current_value)
            selected = (i == self._selected_index)
            style = ''
            if checked:
                style += ' class:radio-checked'
            if selected:
                style += ' class:radio-selected'

            result.append((style, ''))

            if selected:
                result.append(('[SetCursorPosition]', ''))

            display = value[1]
            if checked:
                result.append((style, '->'))
                display = HTML('<style bg="#999" fg="red">{0}</style>'.format(display))
            else:
                result.append((style, '  '))

            result.append((style, ''))
            result.append(('class:radio', ' '))
            result.extend(to_formatted_text(display, style='class:radio'))
            result.append(('', '\n'))

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window