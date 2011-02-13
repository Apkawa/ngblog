# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty
from functools import wraps
from copy import copy
import pkgutil

import logging

log = logging.getLogger('ngblog.plugin')

def not_implemented(func):
    def wrap(*args, **kwargs):
        raise NotImplementedError
    return wrap

class PluginException(Exception):
    #todo: container
    pass

class PluginManager(object):
    __plugins = {}

    def __init__(self):
        self.collect_plugins()

    def collect_plugins(self):
        for module_loader, name, ispkg in pkgutil.iter_modules(['plugins']):
            __import__('.'.join(['plugins',name]))

    @classmethod
    def register(cls, plugin):
        plugin_key = plugin.__module__.split('.')[1]
        cls.__plugins[plugin_key] = plugin
        log.debug('register plugin %s', plugin_key)

    @classmethod
    def get_plugins(cls):
        return cls.__plugins

    @classmethod
    def get_plugin(cls, name):
        return cls.__plugins.get(name)

    @classmethod
    def setup_plugins(cls, settings):
        new_plugins = {}
        for key, plugin in cls.get_plugins().iteritems():
            new_plugins[key] = plugin(settings.get(key))
        return new_plugins

class PluginMetaClass(ABCMeta):
    def __new__(mcls, name, bases, namespace):
        cls = super(PluginMetaClass, mcls).__new__(mcls, name, bases, namespace)
        if not cls.__abstractmethods__:
            mcls.register_plugin(cls)
        return cls

    @classmethod
    def register_plugin(mcls, plugin_class):
        PluginManager.register(plugin_class)


class BasePlugin(object):
    '''Metaclass plugin'''
    __metaclass__ = PluginMetaClass

    default_settings = {}
    required_field = ()

    def __init__(self, settings=None):
        self.settings = copy(self.default_settings)
        if settings and isinstance(settings, dict):
            self.setup(**settings)

    def is_configured(self):
        for r_key in self.required_field:
            if not self.settings.get(r_key):
                return False
        return True

    def setup(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key in self.default_settings:
                self.settings[key] = value

    @property
    def log(self):
        if not hasattr(self, '__logger'):
            self.__logger = logging.getLogger("ngblog.%s"%self.__class__.__module__)
        return self.__logger

    @abstractmethod
    def check_post_id(self, post_id):
        pass

    @abstractmethod
    def check_reply_id(self, reply_id):
        pass

    @abstractmethod
    def add_post(self, text, tags=()):
        pass

    @not_implemented
    def add_reply(self, text, post_id, reply_id=None):
        pass

    @not_implemented
    def get_post(self, post_id):
        pass

    @not_implemented
    def get_reply(self, reply_id):
        pass

    @not_implemented
    def delete_post(self, post_id):
        pass

    @not_implemented
    def delete_reply(self, reply_id):
        pass

def main():
    pass

if __name__ == '__main__':
    main()
