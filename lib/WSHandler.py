#!/usr/bin/env python

from pymongo import Connection

class WSHandler(object):
    def __init__(self):
        conn = Connection()
        self.db = conn[self._DB]

