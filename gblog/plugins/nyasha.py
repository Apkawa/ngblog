# -*- coding: utf-8 -*-

import re
from pyxmpp.jabber.simple import xmpp_do, send_message
from pyxmpp.jid import JID

from pyxmpp.message import Message

from plugin import BasePlugin, not_implemented
from utils import juick_like_message

class XmppDo(object):
    response = False
    def __init__(self, to_jid, from_jid, body):
        self.body = body
        self.to_jid = to_jid
        self.from_jid = from_jid

    def __call__(self, stream):
        message = Message(to_jid=self.to_jid,
                from_jid=self.from_jid, stanza_type='chat', body=self.body)

        stream.set_response_handlers(message, res_handler=self.xmpp_handler,
                err_handler=lambda x: x,)
        stream.send(message)
        while not self.response:
            pass

    def xmpp_handler(self, stanza):
        print stanza
        self.response = True
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
        #xmpp_worker = XmppDo(from_jid=self.settings['jid'], to_jid=self.jabbber_bot_jid, body=text)
        send_message(JID(self.settings['jid']+'/'+self.settings['resource']), 
                self.settings['password'], to_jid=self.jabbber_bot_jid, message_type='chat', body=text)

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
        body = juick_like_message(text, tags)
        self._xmpp_query(body)
        #TODO return id




