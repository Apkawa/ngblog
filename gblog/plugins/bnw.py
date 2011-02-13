# -*- coding: utf-8 -*-
from plugin import BasePlugin, not_implemented

import re
from pyxmpp.jabber.simple import xmpp_do, send_message
from pyxmpp.jid import JID

from pyxmpp.message import Message

class XmppDo(object):
    def __init__(self, body):
        self.body = body

    def __call__(self, stream):
        message = Message(to_jid=self.jabbber_bot_jid,
                from_jid=JID(self.settings['jid']), stanza_type='chat', body=self.body)

        stream.set_response_handlers(message, res_handler=self.xmpp_handler,
                err_handler=lambda x: x,)
        stream.send(message)

    def xmpp_handler(self, stanza):
        print stanza
        pass

class Plugin(BasePlugin):
    '''A http://bnw.im microblog'''
    jabbber_bot_jid = JID('bnw@bnw.im')
    default_settings = {
                'jid':None,
                'password':None,
                'resource':'gblog',
                }

    def _xmpp_query(self, text):
        xmpp_worker = XmppDo(text)
        xmpp_do(JID(self.settings['jid']), self.settings['password'], xmpp_worker)

    #r'^(?:\#|)[A-Z0-9]+(?:\/[A-Z0-9]+|)$'
    def check_post_id(self, post_id):
        '''
        A2YMB6
        '''
        return bool(re.match(r'^[A-Z0-9]+$'))

    def check_reply_id(self, reply_id):
        '''
        DXZ
        '''
        return bool(re.match(r'^[A-Z0-9]+$'))

    def add_post(self, text, tags=()):
        pass

    def add_reply(self, text, post_id, reply_id=None):
        pass

    def get_post(self, post_id):
        pass

    def get_reply(self, reply_id):
        pass



