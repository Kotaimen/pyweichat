# -*- coding: utf-8 -*-

""" A very hackish way to display location based Shanghai traffic data """

from pywc import ReplyTextMessage, ReplyMultiMediaMessage

def reply_text_message(message):
    reply = ReplyTextMessage(message.from_user_name,
                             message.to_user_name,
                             'Please Specify Location Message',
                             )
    return reply.to_weichat()


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


    reply.add_article(u'周边高架信息',
                      u'',
                      u'',
                      u'http://ray.pset.suntec.net/raytrace/highwaypanel?lon=%(lon)s&lat=%(lat)s' \
                      % dict(lon=lon, lat=lat)
                      )
    reply.add_article(u'周边停车场信息',
                      u'',
                      u'',
                      u'http://ray.pset.suntec.net/raytrace/parkinglot?lon=%(lon)s&lat=%(lat)s' \
                      % dict(lon=lon, lat=lat)
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
