# -*- coding: utf-8 -*-

""" A very hackish way to display location based Shanghai traffic data """
import math
import random

from pywc import ReplyTextMessage, ReplyMultiMediaMessage
from grub_jtcx import fetch_panel_list, fetch_parking_list

def reply_text_message(message):
    reply = ReplyTextMessage(message.from_user_name,
                             message.to_user_name,
                             'Please Specify Location Message',
                             )
    return reply.to_weichat()

def distance(lonlat1, lonlat2):
    x1, y1 = lonlat1
    x2, y2 = lonlat2
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

def reply_location_message(message):
    reply = ReplyMultiMediaMessage(message.from_user_name,
                                   message.to_user_name)
    lon, lat = message.location
    reply.add_article(u'当前交通信息',
                      u'经度：%.2f，纬度：%.2f。' % (lon, lat),
                      'http://sis.jtcx.sh.cn/sisserver?config=WMAP&cenX=%(lon)s&cenY=%(lat)s'\
                      '&content=map&width=640&height=400'\
                      '&a_k=7251934c22809062229b12a6d94f26fc6680f1f91572543df145232575be06e920c44e7990ccb51d'\
                      '&showLogo=false&traffic=on&maplevel=4' % dict(lon=lon, lat=lat),

                      'http://ditu.google.cn/maps/api/staticmap?center='\
                      '%(lat)s,%(lon)s&markers=%(lat)s,%(lon)s'\
                      '&zoom=13&size=400x600&sensor=true&visual_refresh&scale=2&language=zh_cn' \
                        % dict(lon=lon, lat=lat),
                      )

    panels = fetch_panel_list(message.location)
    dist = lambda p: distance(p['location'], message.location)
    panels.sort(key=dist)

    for n, panel in enumerate(panels):
        if n >= 4: break
        print panel['name'], panel['image']
        reply.add_article(u'高架：%s' % panel['name'],
                          '',
                          '',
                          panel['image']
                          )

    parkings = fetch_parking_list(message.location)
    dist = lambda p: distance(p['location'], message.location)
    parkings.sort(key=dist)
    count = 0
    for n, parking in enumerate(parkings):
        if parking['available'] <= 1:
            continue
        count += 1
        if count > 5:
            print parking['name'], parking['location'], parking['total'], parking['available']
            continue
        
        reply.add_article(u'停车场：%s（%s），车位：%d，空闲车位：%d' % \
                          (parking['name'], parking['address'], 
                           parking['total'], parking['available']),
                          '',
                          '',
                          'http://ditu.google.cn/maps/api/staticmap?center='\
                          '%(lat)s,%(lon)s&markers=%(lat)s,%(lon)s'\
                          '&zoom=19&size=400x600&sensor=true&visual_refresh&scale=2&language=zh_cn' \
                            % dict(lon=parking['location'][0], lat=parking['location'][1]),
                          )


    return reply.to_weichat()

def test():
    class Message():
        def __init__(self):
            self.from_user_name = 'from'
            self.to_user_name = 'to'
            self.location = (121.533852, 31.268611)
    message = Message()
    print reply_location_message(message)

if __name__ == '__main__':
    test()
