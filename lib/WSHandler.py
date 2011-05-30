#!/usr/bin/env python

from mongoengine import connect, Document, ObjectIdField

def _to_json(data, include_ids=False, sub_documents=False):
    import copy, datetime, time
    
    def _convert_to_json(data):
        struct = {}
#        ignore = ['_id', 'password']
        ignore = []
        for k in data:
            if k in ignore: continue
            value = data[k]
            
            if sub_documents and hasattr(value, "__class__") and issubclass(value.__class__, Document):
                struct[k] = _convert_to_json(value)
            elif isinstance(value, list):
                struct[k] = [_convert_to_json(e) for e in value]
            elif isinstance(value, datetime.datetime):
                struct[k] = int(time.mktime(value.timetuple()) + value.microsecond/1e6)
            elif isinstance(value, (unicode, str)):
                struct[k] = value
        if include_ids:
            id = getattr(data, "id", None)
            struct["id"] = str(id) if id else None
        return struct
    return _convert_to_json(data)

Document.to_json = _to_json

class WSHandler(object):
    def __init__(self):
        connect(self._DB)

