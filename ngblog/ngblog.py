# -*- coding: utf-8 -*-
'''
консольный клиент
'''
import os
import sys

import logging
import plugin
#import settings

import optparse
from optparse import make_option

from utils import parse_message


log = logging.getLogger('ngblog.cli')

class NGBlog(object):
    options = (
            make_option('-s', '--settings', dest='settings', default='settings',
                metavar='SETTINGS', help='Usage settings module'),
            make_option('-v', '--verbose', dest='verbose', default=0, action='store',
                metavar='LEVEL', help='Set verbose level, 1 - INFO; 2 - DEBUG'),
            )

    plugins = plugin.PluginManager()#.setup_plugins(settings.SETTINGS)
    def __init__(self):
        pass

    def parse_args(self):
        plugins = self.plugins

        parse_opt = optparse.OptionParser()
        parse_opt.add_options(self.options)
        for key, p in plugins.get_plugins().iteritems():
            short_key = key[0]
            long_key = key
            parse_opt.add_option('-%s'%short_key, '--%s'%long_key, 
                    action='append_const', const=key, dest='plugins', help=p.__doc__)

        options, args = parse_opt.parse_args(sys.argv[1:])

        if not options.plugins:
            options.plugins = plugins.get_plugins().keys()
        logging.basicConfig(level=logging.DEBUG)
        log.debug('parsing args: %s options: %s', args, options )
        return args, options

    def get_text(self, args):
        if args and args[0] != '-':
            log.debug('Open file %s', args[0])
            text = open(args[0], 'rb').read()
        else:
            log.debug('Read from stdin')
            text = sys.stdin.read()

        return text

    def process(self, text, options):
        plugins = self.plugins

        settings = self.load_settings(options.settings)

        log.info('Load `%s` settings.', options.settings)
        log.debug('Settings dict %s', settings)

        plugins_instances = plugins.setup_plugins(settings)
        tags, text = parse_message(text)

        log.debug("Parsed text: tags: %s; text: %s",tags, text)

        for key in options.plugins:
            p = plugins_instances.get(key)
            if p.is_configured():
                p.add_post(text, tags)
                pass
            else:
                log.warning('Plugin %s not valid configuration', key)

    def run(self):
        args, options = self.parse_args()
        text = self.get_text(args)
        self.process(text, options)




    def load_settings(self, settings_name):
        settings_module = __import__(settings_name)
        return getattr(settings_module, 'SETTINGS')

def main():
    ng = NGBlog()
    ng.run()
    '''
    tags, text = parse_message(sys.argv[1])
    for key, plug in plugins.iteritems():
        if plug.is_configured():
            plug.add_post(text, tags)
    '''
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
