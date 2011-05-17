#!/usr/bin/env python

from pymongo import Connection

from tornadorpc.json import JSONRPCHandler
from tornadorpc import private, start_server

class WSHandler(JSONRPCHandler):
    def __init__(self, *args, **kwargs):
        super(JSONRPCHandler, self).__init__(*args, **kwargs)
        conn = Connection()
        self.db = conn[self._DB]

class Handler(WSHandler):
    _DB = "test"

    def add(self, msg):
        message = { "content": msg }
        self.db.messages.insert(message)
        return True

    def all(self):
        messages = [{ "content": m["content"] } for m in self.db.messages.find()]
        return messages

start_server(Handler, port=8080)
