# -*- coding: utf-8 -*-

import re

MAX_TAG_COUNT = 5
SPLIT_MESSAGE_REGEXP = re.compile('^\s*(?:\*\S+\s+){,%s}'%MAX_TAG_COUNT)
SPLIT_TAG_REGEXP = re.compile('(?:\*([\S]+)|\S.*)')
def parse_message(body):
    '''
    Парсит сообщение на тело сообщения и теги.
    формат входного сообщения - 
    *tag *tag2 *tags Тело сообщения
    '''
    body = body.strip()
    tags = SPLIT_MESSAGE_REGEXP.match(body).group(0)
    message = body[len(tags):]
    tags_set = SPLIT_TAG_REGEXP.findall(tags)
    return tags_set, message

def juick_like_message(text, tags, delim='\n'):
    '''
    Составляет juick like сообщение
    '''
    return delim.join([' '.join('*%s'%t for t in tags), text])
