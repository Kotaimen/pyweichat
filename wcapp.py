#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Weichat app
'''

import ast

from flask import Flask, request
from pywc import *


def reply_text_message(message):
    reply = ReplyTextMessage(message.from_user_name,
                             message.to_user_name,
                             'Please Specify Location Message',
                             )
    return reply.to_weichat()

def reply_location_message(message):
    reply = ReplyMultiMediaMessage(message.from_user_name,
                                   message.to_user_name)

    reply.add_article('Location', str(message.location),
                      'http://navicloud.pset.suntec.net:7198/tile/Terrain/2/1/1.jpg',
                      'http://navicloud.pset.suntec.net/maps/2d')

    return reply.to_weichat()

app = Flask(__name__)

TOKEN = '123456'

@app.route('/raytrace', methods=['GET', 'POST'])
def weichatapp():
    try:
        server_authentication(TOKEN, request.args)
    except AuthenticationError:
        return 'Unauthorized', 401

    if request.method == 'GET':
        return request.args['echostr'], 200
    elif request.method == 'POST':
        reply_header = {'Content-Type': 'appication/xml'}
        message = post_message_factory(request.data)

        if isinstance(message, PostTextMessage):
            reply = reply_text_message(message)
            return reply, 200, reply_header
        elif isinstance(message, PostLocationMessage):
            reply = reply_location_message(message)
            return reply, 200, reply_header
        else:
            return 'Not Implemented', 501


    else:
        return 'Method Not Allowed', 405

app.debug = True
app.run(host='0.0.0.0')
