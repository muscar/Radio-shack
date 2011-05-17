#!/usr/bin/env python

from tornadorpc import private, start_server

from lib.WSHandler import WSHandler

class Handler(WSHandler):
    _DB = "test"

    def add(self, msg):
        message = { "content": msg }
        self.db.messages.insert(message)
        return True

    def all(self):
        messages = [{ "content": m["content"] } for m in self.db.messages.find()]
        return messages

start_server(Handler, port=8000)
