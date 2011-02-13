# -*- coding: utf-8 -*-

import re
import os
import json
import urllib

from pyxmpp.jabber.simple import xmpp_do, send_message
from pyxmpp.jid import JID

from pyxmpp.message import Message

from plugin import BasePlugin, not_implemented
from utils import juick_like_message


class Plugin(BasePlugin):
    '''A http://bnw.im microblog'''
    api_url = 'http://bnw.im/api/'
    default_settings = {
                'login_key':None,
                }
    required_field = ('login_key',)

    def api_query(self, url, data):
        post_data = urllib.urlencode(data)
        self.log.debug('api query: %s?%s', url, post_data)
        response = urllib.urlopen(url, post_data)
        src = response.read()
        self.log.debug('response: %s', src)
        r = json.loads(src)
        return r


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
        url = os.path.join(self.api_url, 'post')
        data = {'login':self.settings['login_key']}
        data['text'] = text
        data['tags'] = ','.join(tags)
        response = self.api_query(url, data)
        if response['ok']:
            return response['id']

    def add_reply(self, text, post_id, reply_id=None):
        url = os.path.join(self.api_url, 'comment')
        data = {'login':self.settings['login_key']}
        data['message'] = post_id
        if reply_id:
            data['message'] += "/%s"%reply_id
        data['text'] = text
        response = self.api_query(url, data)
        if response['ok']:
            return response['id']

    def get_post(self, post_id):
        url = os.path.join(self.api_url, 'show')
        data = {}
        data['message'] = post_id
        response = self.api_query(url, data)
        if response['ok']:
            return response

    def get_reply(self, reply_id):
        url = os.path.join(self.api_url, 'show')
        data = {}
        data['message'] = reply_id
        response = self.api_query(url, data)
        if response['ok']:
            return response

    def delete_post(self, post_id):
        url = os.path.join(self.api_url, 'delete')
        data = {'login':self.settings['login_key']}
        data['message'] = post_id
        response = self.api_query(url, data)
        if response['ok']:
            return response

    def delete_reply(self, reply_id):
        url = os.path.join(self.api_url, 'delete')
        data = {'login':self.settings['login_key']}
        data['message'] = reply_id
        response = self.api_query(url, data)
        if response['ok']:
            return response




