#!/usr/bin/env python

from tornadorpc import private, start_server
from tornadorpc.json import JSONRPCHandler

from pymongo.objectid import ObjectId

from lib.WSHandler import WSHandler

import models

def decode_seq(model_builder, seq):
    """Transforms a list of dictionaries into a list of models."""
    if seq is not None:
        return [model_builder(**e) for e in seq]
    return []

class Radio(WSHandler):
    _DB = "radioshack"

    def add(self, name, freqs=None, streams=None):
        radio = models.Radio(name=name,
                            frequencies=decode_seq(models.RadioFreq, freqs),
                            streams=decode_seq(models.RadioStream, streams))
        radio.save()
        return str(radio.id)

    def update(self, id, name=None, freqs=None, streams=None):
        dirty = False
        radio = models.Radio.objects.with_id(id)
        if name is not None:
            radio.name = name
            dirty = True
        if freqs is not None:
            radio.frequencies = decode_seq(models.RadioFreq, freqs)
            dirty = True
        if streams is not None:
            radio.streams = decode_seq(models.RadioStream, streams)
            dirty = True
        if dirty:
            radio.save()
        return dirty

    def remove(self, id):
        models.Radio.objects.with_id(id).delete()
        return True

    def all(self):
        return [r.to_json(include_ids=True)
                for r in models.Radio.objects.all()]

class Show(WSHandler):
    _DB = "radioshack"

    def add(self, name, description=None, photoUrl=None, hosts=None):
        show = models.Show(name=name,
                           description=description,
                           photoUrl=photoUrl,
                           hosts=decode_seq(models.ShowHost, hosts))
        show.save()
        return str(show.id)

    def update(self, id, name=None, desc=None, photoUrl=None, hosts=None):
        dirty = False
        show = models.Show.objects.with_id(id)
        if name is not None:
            show.name = name
            dirty = True
        if desc is not None:
            show.description = desc
            dirty = True
        if photoUrl is not None:
            show.photoUrl = photoUrl
            dirty = True
        if hosts is not None:
            show.hosts = decode_seq(models.ShowHost, hosts)
            dirty = True
        if dirty:
            show.save()
        return dirty

    def remove(self, id):
        models.Show.objects.with_id(id).delete()
        return True

    def all(self):
        return [s.to_json(include_ids=True)
                for s in models.Show.objects.all()]
        
class Handler(JSONRPCHandler):
    radio = Radio()
    show = Show()

start_server(Handler, route="/api/", port=8000)
