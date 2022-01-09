
# Infront Connect Market Data Simulator

This project demonstrates how to use `Infront Connect Market Data` APIs provided by [InfrontServices](https://www.infrontfinance.com/).

* Communication protocol is Websocket
* `server` (simulator of Infront server)
    * `server` is built as a skeleton, which can be  extended by following this [note](##Extend-server)
    * It reponses to incoming requests at different endpoints (paths).
    * `server` will broadcast (streaming) data to registered `consumer`(s). Another streaming stragety such as round-robin can be easily implemented.

* The first ever `consumer` sends a login request to `server` and gets back a valid `session_token`, which is saved at `active_session.json`. Other `consumers` skips this step and uses the saved `session_token` when communicating with the `server`.

* All `consumer`s registers itself with the `sever` and then directly consumes (streaming) data sent from `server`.

### Run the project

- Optionally, go to `constants.py` to change login id and password. It does not matter in order to run the project.
- `pip install -r requirements.txt`
- Start sever by `./server.py`
- Start a consumer by `./consumer.py`. It is possible to start multiple consumers and they all get the same data as `server` broadcasts messages.

### Extend server

### References
https://software.infrontservices.com/developer/Infront%20Connect%20Market%20Data%20API.html