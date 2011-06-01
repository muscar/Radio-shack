#!/usr/bin/env python

from mongoengine import connect, Document, EmbeddedDocument, fields, ObjectIdField
from argparse import ArgumentError

def __to_json(data, include_ids=False, sub_documents=False):
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
            elif sub_documents and issubclass(value.__class__, EmbeddedDocument):
                struct[k] = _convert_to_json(value)
            elif isinstance(value, list):
                struct[k] = [_convert_to_json(e) for e in value]
            elif isinstance(value, datetime.datetime):
                struct[k] = int(time.mktime(value.timetuple()) + value.microsecond/1e6)
            else:
                struct[k] = value
        if include_ids:
            id = getattr(data, "id", None)
            struct["id"] = str(id) if id else None
        return struct
    return _convert_to_json(data)

def _from_json(cls, data):
    def decode_seq(model_builder, seq):
        """Transforms a list of dictionaries into a list of models."""
        if seq is not None:
            return [model_builder(**e) for e in seq]
        return []
    def decode_dict(model_builder, data):
        aux = {}
        for k, v in data.iteritems():
            field = model_builder._fields.get(k)
            if field is None:
                raise Exception("{0} does not have a field called {1}".format(model_builder.__name__, k))
            if isinstance(field, fields.ListField):
                aux[k] = decode_seq(field.field.document_type_obj, v)
            elif isinstance(field, fields.EmbeddedDocumentField):
                aux[k] = decode_dict(field.document_type_obj, v)
            else:
                aux[k] = v
        return model_builder(**aux)
    if isinstance(data, list):
        return decode_seq(cls, data)
    elif isinstance(data, dict):
        return decode_dict(cls, data)
    else:
        return data

Document.to_json = __to_json
Document.from_json = classmethod(_from_json)

class WSHandler(object):
    def __init__(self):
        connect(self._DB)

class CRUDHandler(WSHandler):
    def __init__(self):
        super(CRUDHandler, self).__init__()
        
    def create(self, args):
        if not args:
            return None 
        inst = self._MODEL.from_json(args)
        inst.save()
        return str(inst.id)
    
    def read(self):
        return [r.to_json(include_ids=True, sub_documents=True)
                for r in self._MODEL.objects.all()]
        
    def update(self, id, args):
        if not args:
            return False
        inst = self._MODEL.objects.with_id(id)
        for k, v in args.iteritems():
            inst[k] = _from_json(self._MODEL._fields[k].field.document_type_obj, v)
        inst.save()
        return True
    
    def delete(self, id):
        self._MODEL.objects.with_id(id).delete()
        return True
