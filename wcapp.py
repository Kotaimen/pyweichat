#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Weichat app
'''

import ast

from flask import Flask, request
from flask.ext.cache import Cache
from flask import render_template

from pywc import *
from wc_jtcx import *
from parkinglot import *
from highwaypanel import *

app = Flask(__name__, static_folder="static", static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

TOKEN = '123456'


@app.route('/')
def root():
    return 'ok', 200


@app.route('/raytrace', methods=['GET', 'POST'])
def weichatapp():
    try:
        server_authentication(TOKEN, request.args)
    except AuthenticationError:
        app.logger.error('Server authentication failed!')
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


@app.route('/raytrace/parkinglot')
def parkinglot():
    lon = request.args.get('lon')
    lat = request.args.get('lat')

    if lon is None or lat is None:
        return 'Bad Request', 400

    location = float(lon), float(lat)
    service = ParkingLotService()
    parkinglots = service.fetch(location)

    return render_template('parkinglot.html', parkinglots=parkinglots)


@app.route('/raytrace/highwaypanel')
def highwaypanel():
    lon = request.args.get('lon')
    lat = request.args.get('lat')

    if lon is None or lat is None:
        return 'Bad Request', 400
    
    location = float(lon), float(lat)
    service = HighwayPanelService()
    panels = service.fetch(location)

    return render_template('highwaypanel.html', panels=panels)


app.debug = True
app.run(host='0.0.0.0')
