#!/usr/bin/env python

import asyncio
from asyncio.tasks import sleep
import websockets
import json
import constants
import time

SERVER_URL = 'ws://localhost:8765'
LOGIN_REQUEST = {
    "request_data": "ValueToBeReturnedInResponse",
    "md_login_request":
    {
        "login_id": constants.LOGIN_ID,
        "password": constants.LOGIN_PASSWORD,
        "client_application": "WEB",
        "client_application_version": "1.0",
        "country_code": "no",
        "language_code": "en"
    }
}
class ClientSession(object):
    token = None
    timeout = 0
    time_to_live = constants.TIME_TO_LIVE
    is_registered = False

async def login(session):
    print('Start Login job')
    async with websockets.connect(SERVER_URL + '/md_login_request') as websocket:
        await websocket.send(json.dumps(LOGIN_REQUEST))
        response = await websocket.recv()
        login_response = json.loads(response)
        if login_response['error_code'] == 0:
            session.token = login_response['session_token']
            session.timeout = login_response['md_login_response']['session_timeout']
            with open('active_session.json', 'w') as f:
                f.write(json.dumps({"session_token" : session.token, "session_timeout": session.timeout}))
            print('Login was succesfull ! with ' + session.token)
        else:
            print('Login failed !')

async def register(session, websocket):
    if session.token and session.token != "0":
        if not session.is_registered:
            print('Inform server that I am logged in and ready')
            await websocket.send(json.dumps({"session_token": session.token}))
            session.is_registered = True
    else:
        print('Not be able to login yet')

async def consumer(session):
    start = time.time()
    elapsed = 0
    async with websockets.connect(SERVER_URL + '/md_instrument_update') as websocket:
        while elapsed < session.time_to_live:
            elapsed = time.time() - start
            if session.token and session.token != "0":
                if not session.is_registered:
                    print('Inform server that I am logged in and ready')
                    await websocket.send(json.dumps({"session_token": session.token}))
                    session.is_registered = True
            else:
                print('Not be able to login yet')
            if session.is_registered:
                instrument_update = await websocket.recv()
                print('Receiving ' + instrument_update)
            await asyncio.sleep(0.5)
        print('Bye ! I am going away')

def main():
    with open('active_session.json') as f:
        active_session = json.loads(f.read())
        client_session = ClientSession()
        client_session.token = active_session['session_token']
        client_session.timeout = active_session['session_timeout']
        # Login if not yet
        if client_session.token == "0":
            asyncio.get_event_loop().create_task(login(client_session))

        asyncio.get_event_loop().run_until_complete(consumer(client_session))
        #asyncio.get_event_loop().run_until_complete()

if __name__ == "__main__":
    main()