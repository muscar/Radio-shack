import datetime

import mongoengine as db

class RadioFreq(db.EmbeddedDocument):
    location = db.StringField(max_length=50)
    title = db.StringField(max_length=50)

class RadioStream(db.EmbeddedDocument):
    url = db.StringField(max_length=50)
    quality = db.StringField(max_length=50)

class Radio(db.Document):
    name = db.StringField(max_length=50, required=True)
    frequencies = db.ListField(db.EmbeddedDocumentField(RadioFreq))
    streams = db.ListField(db.EmbeddedDocumentField(RadioStream))
    
class ShowHost(db.EmbeddedDocument):
    name = db.StringField(max_length=50, required=True)
    description = db.StringField(max_length=50)
    photoUrl = db.StringField(max_length=50)

class Show(db.Document):
    name = db.StringField(max_length=50, required=True)
    description = db.StringField(max_length=50)
    photoUrl = db.StringField(max_length=50)
    hosts = db.ListField(db.EmbeddedDocumentField(ShowHost))
    time = db.DateTimeField(default=datetime.datetime.now)
