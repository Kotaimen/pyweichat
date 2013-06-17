# -*- coding: utf-8 -*-

'''
Created on Jun 17, 2013

@author: Kotaimen
'''

import time
import math
import collections
import xml.etree.ElementTree as etree

#===============================================================================
# Post messages
#===============================================================================

class PostTextMessage(collections.namedtuple('PostTextMessage', '''from_user_name
    to_user_name timestamp message_id message''')):
    """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
    </xml>
    """
    __slots__ = ()
    pass


class PostLocationMessage(collections.namedtuple('PostTextMessage', '''from_user_name
    to_user_name timestamp message_id location scale''')):
    """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>23.134521</Location_X>
        <Location_Y>113.358803</Location_Y>
        <Scale>20</Scale>
        <Label><![CDATA[位置信息]]></Label>
        <MsgId>1234567890123456</MsgId>
    </xml>
    """
    __slots__ = ()
    pass


def post_message_factory(data):
    tree = etree.fromstring(data)
    message_type = tree.find('MsgType').text
    from_user_name = tree.find('FromUserName').text
    to_user_name = tree.find('ToUserName').text
    timestamp = int(tree.find('CreateTime').text)

    if message_type == 'text':
        message_id = tree.find('MsgId').text
        content = tree.find('Content').text

        return PostTextMessage(from_user_name, to_user_name,
                               timestamp, message_id, content)
    elif message_type == 'location':
        message_id = tree.find('MsgId').text
        scale = int(tree.find('Scale').text)
        lat = float(tree.find('Location_X').text)  # No idea why X is latitude...
        lon = float(tree.find('Location_Y').text)
        location = (lat, lon)
        return PostLocationMessage(from_user_name, to_user_name,
                                   timestamp, message_id, location, scale)

    else:
        assert False, 'unsupported message type'

#===============================================================================
# Reply messages
#===============================================================================

class ReplyTextMessage(object):
    def __init__(self, from_user_name, to_user_name, message):
        self.timestamp = math.floor(time.time())
        self.from_user_name = from_user_name
        self.to_user_name = to_user_name
        self.message = message

    def to_weichat(self):
        return '''<xml><ToUserName><![CDATA[%(from_user_name)s]]></ToUserName>
<FromUserName><![CDATA[%(to_user_name)s]]></FromUserName>
<CreateTime>%(timestamp)d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%(message)s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>''' % { 'from_user_name': self.from_user_name,
              'to_user_name': self.to_user_name,
              'timestamp': self.timestamp,
              'message': self.message, }



class ReplyMultiMediaMessage(object):
    def __init__(self, from_user_name, to_user_name):
        self.timestamp = math.floor(time.time())
        self.from_user_name = from_user_name
        self.to_user_name = to_user_name
        self.articles = list()

    def add_article(self, title, description, picture_url, link):
        self.articles.append((title, description, picture_url, link))

    def to_weichat(self):
        num_articles = len(self.articles)
        assert num_articles > 0
        assert num_articles <= 10

        reply = '''<xml><ToUserName><![CDATA[%(from_user_name)s]]></ToUserName>
<FromUserName><![CDATA[%(to_user_name)s]]></FromUserName>
<CreateTime>%(timestamp)d</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>%(num_articles)d</ArticleCount>
<Articles>''' % { 'from_user_name': self.from_user_name,
                'to_user_name': self.to_user_name,
                'timestamp': self.timestamp,
                'num_articles': num_articles, }

        for title, description, picture_url, link in self.articles:
            reply += '''<item>
 <Title><![CDATA[%(title)s]]></Title>
 <Description><![CDATA[%(description)s]]></Description>
 <PicUrl><![CDATA[%(picture_url)s]]></PicUrl>
 <Url><![CDATA[%(link)s]]></Url>
 </item>''' % {'title': title,
               'description': description,
               'picture_url': picture_url,
               'link': link,
               }

        reply += '''/<Articles>
<FuncFlag>0</FuncFlag>
</xml>'''
        return reply
