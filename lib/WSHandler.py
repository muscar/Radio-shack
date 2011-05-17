#!/usr/bin/env python

from pymongo import Connection

from tornadorpc.json import JSONRPCHandler

class WSHandler(JSONRPCHandler):
    def __init__(self, *args, **kwargs):
        super(JSONRPCHandler, self).__init__(*args, **kwargs)
        conn = Connection()
        self.db = conn[self._DB]

