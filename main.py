#!/usr/bin/env python

from tornadorpc import private, start_server
from tornadorpc.json import JSONRPCHandler

from pymongo.objectid import ObjectId

from lib.WSHandler import WSHandler
from lib import db

import models

class Radio(WSHandler):
    _DB = "radioshack"

    def add(self, name, freqs=None, streams=None):
        radio = { "name": name,
                  "frequencies": freqs or [],
                  "streams": streams or [] }
        if not db.check_model(radio, models.Radio):
            raise TypeError("bad arguments")
        id = self.db.radios.insert(radio)
        return str(id)

    def update(self, id, name=None, freqs=None, streams=None):
        details = { "name": name } if name else {}
        if freqs is not None:
            details["freqs"] = freqs
        if streams is not None:
            details["streams"] = streams
        if details:
            if not db.check_model(details, models.Radio,
                                  allow_missing_members=True):
                raise TypeError("bad arguments")
            self.db.radios.update({ "_id": ObjectId(id) },
                                  { "$set": details })
            return True
        return False

    def remove(self, id):
        return self.db.radios.remove({ "_id": ObjectId(id) })

    def all(self):
        radios = list(self.db.radios.find())
        for r in radios:
            r["_id"] = str(r["_id"])
        return radios

class Show(WSHandler):
    _DB = "radioshack"

    def add(self, title, desc, photo=None, hosts=None, time=None):
        show = { "title": title,
                 "desc": desc,
                 "photo": photo,
                 "hosts": hosts or [],
                 "time": time }
        id = self.db.shows.insert(show)
        return str(id)

    def update(self, id, title=None, desc=None, photo=None, hosts=None, time=None):
        details = { "title": title } if title else {}
        if freqs is not None:
            details["freqs"] = freqs
        if streams is not None:
            details["streams"] = streams
        if details:
            self.db.radios.update({ "_id": ObjectId(id) }, { "$set": details })
            return True
        return False

    def remove(self, id):
        return self.db.radios.remove({ "_id": ObjectId(id) })

    def all(self):
        radios = list(self.db.radios.find())
        for r in radios:
            r["_id"] = str(r["_id"])
        return radios

class Handler(JSONRPCHandler):
    radio = Radio()

start_server(Handler, route="/api/", port=8000)
