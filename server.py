#!/usr/bin/env python

import asyncio
from asyncio.events import get_event_loop
import websockets
import json
import sys
import constants

current_module = sys.modules[__name__]
SESSION_TOKEN = '9b6aa578-2320-48f2-903a-359e380369c0'

USERS_WEBSOCKETS = {'websockets':[]}

SUBSCRIPTION_DATABASE = {
        # Default data
        "update_data": "oslo",
        "fields": ["BID", "ASK", "TIME", "LAST", "CHANGE", "PCT_CHANGE"],
        "instruments": [{ "feed": 18177, "ticker": "STL" }, { "feed": 18177, "ticker": "REC" }]
    }


def md_login_request(websocket, path, request):
    if (request['md_login_request']['login_id'] == constants.LOGIN_ID and 
        request['md_login_request']['password'] == constants.LOGIN_PASSWORD):
        return {
            "request_data": "ValueToBeReturnedInResponse",
            "error_code": 0,
            "session_token": SESSION_TOKEN,
            "md_login_response": {
                "version": "1.3.1",
                "build": "mobile_and_web_server 0.3.0 PRIVATE BUILD",
                "remote_address": "1.2.3.4",
                "session_timeout": 900000,
                "session_token": SESSION_TOKEN,
                "features": ["INFINANCIALS", "TWEETWIRES"],
                "logical_session_token": "9b6bc578-1234-48f2-903a-359e365769c2"
            }
        }
    else:
        return {
        "request_data": "ValueToBeReturnedInResponse",
        "error_code": 403,
        "error_message": "Your account is not set up with Infront Connect API access.",
        "md_login_response": {
            "version": "1.10.1",
            "build": "mobile_and_web_server v8.8.0.44 (2021-12-22 14:05:51Z)",
            "remote_address": "84.218.xxx.xxx"
        }
    }

def md_subscribe_instrument_request(websocket, path, request):
    subscribe_instrument_request = request['md_subscribe_instrument_request']
    SUBSCRIPTION_DATABASE['update_data'] = subscribe_instrument_request['update_data']
    SUBSCRIPTION_DATABASE['fields'] = subscribe_instrument_request['fields']
    SUBSCRIPTION_DATABASE['instruments'] = subscribe_instrument_request['instruments']

    return {
        "error_code": 0,
        "session_token": SESSION_TOKEN,
        "md_subscribe_instrument_response": {}
    }

def md_instrument_update(websocket, path, request):
    # save websocket if the session_token is valid
    session_token = request['session_token']
    print(session_token)
    if session_token == SESSION_TOKEN:
        print('Register a consumer')
        USERS_WEBSOCKETS['websockets'].append(websocket)

def process_message(websocket, path, message):
    request = json.loads(message)
    response = getattr(current_module, path[1:])(websocket, path, request)
    return json.dumps(response)

async def producer():
    print('Start Producer job')
    while True:
        for websocket in USERS_WEBSOCKETS['websockets']:
            from datetime import datetime
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            print(f'Sending {date_time}')
            await websocket.send(date_time)
        await asyncio.sleep(0.5)  # run forever

async def handler(websocket, path):
    print(f'Serving request at {path}')
    async for message in websocket:
        response = process_message(websocket, path, message)
        if response:
            await websocket.send(response)

async def ping_pong():
    print('Start Handler job')
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.get_event_loop().create_task(ping_pong())
asyncio.get_event_loop().create_task(producer())
asyncio.get_event_loop().run_forever()

