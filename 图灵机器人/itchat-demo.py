# https://github.com/littlecodersh/ItChat
import itchat

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return '你说?: ' + msg.text

itchat.auto_login(enableCmdQR=False)
itchat.run()
itchat.logout()