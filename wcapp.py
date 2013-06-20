#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Weichat app
'''

import ast

from flask import Flask, request
from pywc import *
from wc_jtcx import *



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
