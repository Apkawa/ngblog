# -*- coding: utf-8 -*-
'''
консольный клиент
'''
import os
import sys

import logging
import plugin
import settings
from utils import parse_message

logging.basicConfig(level=logging.DEBUG)

def main():
    plugins = plugin.PluginManager().setup_plugins(settings.SETTINGS)
    tags, text = parse_message(sys.argv[1])
    for key, plug in plugins.iteritems():
        if plug.is_configured():
            plug.add_post(text, tags)

    #bnw = plugins.get('bnw')
    #post_id = bnw.add_post('Tect bnw api', ['test'])
    #psto = plugins.get('psto')
    #if psto.is_configured():
    #    psto.add_post('Привет, это тест супер либы', ['*', 'nya'])
    #nyasha = plugins.get('nyasha')
    #if nyasha.is_configured():
    #    nyasha.add_post('Привет, это тест супер либы', ['*', 'nya'])
    #juick = plugins.get('juick')
    #if juick.is_configured():
    #    juick.add_post('Привет, это тест супер либы', ['*', 'nya'])

    #reply_id = bnw.add_reply('Tect bnw api', 'JPWL85')

    #reply_id = bnw.add_reply('Tect bnw api', 'JPWL85/FWH')
    #print bnw.get_reply(reply_id)
    #print bnw.delete_reply(reply_id)
    #print bnw.delete_post(post_id)



if __name__ == '__main__':
    main()
