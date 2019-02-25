# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import json
import os
import sys
import time
from argparse import ArgumentParser
from datetime import datetime
from threading import Thread

import pychromecast
import requests
from flask import Flask, abort, jsonify, request, send_from_directory, render_template

#local module
from googlehome import voice_cast
from lineapi import line_bot_api,parser


CACHE_DIR = "cache"
CACHE_WIPE_INTERVAL = 60 * 5

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Avoid garbled characters

URL = "http://raspi-homecontrol.mydns.jp"



@app.route("/callback", methods=['POST'])
def callback():
    
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    return 'OK'


@app.route("/")
def index():
    return "Hi There"


@app.route("/database")
def database():
    db = {"_default": {"1": {"name": "Light", "power": "000111"},
                       "2": {"name": "TV", "power": "121212", "volume_up": "222211"}}}

    return render_template("index.html", message=db)


@app.route("/test")
def test():
    voice_cast().play_text("テストボイスです")
    return "test voice play"


@app.route("/cache/<path:path>")
def send_cache(path):
    return send_from_directory("cache", path)


@app.route("/ifttt_json", methods=["POST"])
def ifttt():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify(res='error'), 400
    print(request.json)
    return jsonify(res='ok')


"""
def wipe_cache_task():
    print("Cache wiping task started. Cache wiping interval is {} seconds.".format(CACHE_WIPE_INTERVAL))
    while True:
        for path in os.listdir(CACHE_DIR):
            os.remove("{}/{}".format(CACHE_DIR,path))
        time.sleep(CACHE_WIPE_INTERVAL)
"""

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int,
                            default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    # Thread(target=wipe_cache_task).start()
    app.run(debug=True)
