#!/usr/bin/env python

from tornadorpc import private, start_server
from tornadorpc.json import JSONRPCHandler

from pymongo.objectid import ObjectId

from lib.WSHandler import CRUDHandler

import models

class Radio(CRUDHandler):
    _DB = "radioshack"
    _MODEL = models.Radio
    
class Show(CRUDHandler):
    _DB = "radioshack"
    _MODEL = models.Show
    
class Handler(JSONRPCHandler):
    radio = Radio()
    show = Show()

start_server(Handler, route="/api/", port=8000)
