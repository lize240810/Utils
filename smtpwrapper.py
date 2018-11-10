# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#https://docs.python.org/2/library/email-examples.html#email-examples
#http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832745198026a685614e7462fb57dbf733cc9f3ad000

import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

class SMTPWrapper(object):
    '''SMTP邮件发送包装类'''
    def __init__(self, server='localhost', port=25, username=None, password=None, debug=False):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.debug = debug

        self.from_msg = 'from'
        self.to_msg = 'to'

    def send(self, receiver, message='Default Message', subject='Default Title', html=False, from_msg=None, to_msg=None):
        '''发送'''
        def _format_addr(_addr):
            name, addr = parseaddr(_addr)
            return formataddr(
                (
                    Header(name, 'utf-8').encode(),
                    addr
                )
            )

        msg_type = 'html' if html else 'plain'
        msg = MIMEText(message, msg_type, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8').encode()
        _from_msg = self.from_msg if from_msg is None else from_msg
        msg['From'] = _format_addr('{from_msg} <{sender}>'.format(from_msg=_from_msg, sender=self.username))
        _to_msg = self.to_msg if to_msg is None else to_msg
        msg['To'] = _format_addr('{to_msg} <{receiver}>'.format(to_msg=_to_msg, receiver=receiver))
        
        srv = smtplib.SMTP(self.server, self.port)
        srv.set_debuglevel(self.debug)
        srv.login(self.username, self.password)
        srv.sendmail(self.username, [receiver], msg.as_string())
        srv.quit()

if __name__ == '__main__':
    demo = SMTPWrapper(
        server='smtp.163.com',
        username='xxx@163.com',
        password='xxx',
        debug=True
    )
    msg = 'hello, smtplib of Python! <br />中文测试'
    demo.send(
        'xxx@xxx.com',
        message=''.join([
            '<div>',
            '<strong>',
            msg,
            '</strong>',
            '</div>'
        ]),
        html=True
    )
