# -*- coding: utf-8 -*-

import re
from pyxmpp.jabber.simple import xmpp_do, send_message
from pyxmpp.jid import JID

from pyxmpp.message import Message

from plugin import BasePlugin, not_implemented
from utils import juick_like_message

class Plugin(BasePlugin):
    '''A http://psto.net microblog'''
    jabbber_bot_jid = JID('psto@psto.net')
    default_settings = {
                'jid':None,
                'password':None,
                'resource':'gblog',
                }
    required_field = ('jid','password')

    def _xmpp_query(self, text):
        send_message(JID(self.settings['jid']+'/'+self.settings['resource']), 
                self.settings['password'], to_jid=self.jabbber_bot_jid, message_type='chat', body=text)

    def check_post_id(self, post_id):
        '''
        hfgnh
        '''
        return bool(re.match(r'^[a-z]+$'))

    def check_reply_id(self, reply_id):
        '''
        12
        '''
        return bool(re.match(r'^[0-9]+$'))

    def add_post(self, text, tags=()):
        body = juick_like_message(text, tags, delim='//')
        self._xmpp_query(body)
        #TODO return id

    @not_implemented
    def add_reply(self, text, post_id, reply_id=None):
        body = juick_like_message(text, tags, delim='//')
        self._xmpp_query(body)
        #TODO return id




