# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty
from functools import wraps
from copy import copy

def not_implemented(func):
    def wrap(*args, **kwargs):
        raise NotImplementedError
    return wrap

class PluginManager(object):
    __plugins = {}

    def __init__(self):
        self.collect_plugins()

    def collect_plugins(self):
        import plugins.bnw

    @classmethod
    def register(cls, plugin):
        cls.__plugins[plugin.__module__] = plugin

    @classmethod
    def get_plugins(cls):
        return cls.__plugins

#plugin_manager = PluginManager()


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

    def __init__(self):
        self.settings = copy(self.default_settings)

    def setup_settings(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key in self.default_settings:
                self.settings[key] = value

    @abstractmethod
    def check_post_id(self, post_id):
        pass

    @abstractmethod
    def check_reply_id(self, reply_id):
        pass

    @abstractmethod
    def add_post(self, text, tags=()):
        pass

    @abstractmethod
    def add_reply(self, text, post_id, reply_id=None):
        pass

    @abstractmethod
    def get_post(self, post_id):
        pass

    @abstractmethod
    def get_reply(self, reply_id):
        pass

    @not_implemented
    def delete_post(self, post_id):
        pass

    @not_implemented
    def delete_replt(self, reply_id):
        pass

def main():
    pass

if __name__ == '__main__':
    main()
