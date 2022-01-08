
# Infront Connect Market Data Simulator

This project demonstrate how to use `Infront Connect Market Data` APIs provided by [InfrontServices](https://www.infrontfinance.com/).

* Communication protocol is Websocket
* `server` (simulator of Infront erver) is built as a skeleton to be easily extended. 

    It reponses to incoming requests at different endpoints (paths).

    `server` will broadcast (streaming) data to registered `consumer`(s).

* The first ever `consumer` sends a login request to `server` and gets back a valid `session_token`, which is saved at `active_session.json`. Other `consumers` skips this step and uses the saved `session_token` when communicating with the `server`.

* All `consumer`s registers itself with the `sever` and then directly consumes (streaming) data sent from `server`.

### How to use

- Notice `constants.py` to change login id and password.
- pip install -r requirements.txt
- Start sever by `./server.py`
- Start a consumer by `./consumer.py`
It is possible to start multiple consumers and they all get the same data as `server` broadcasts messages.


### APIs
https://software.infrontservices.com/developer/Infront%20Connect%20Market%20Data%20API.html