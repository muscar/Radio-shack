import datetime

import mongoengine as db

# Radios

class RadioFreq(db.EmbeddedDocument):
    location = db.StringField(max_length=50)
    title = db.StringField(max_length=50)

class RadioStream(db.EmbeddedDocument):
    url = db.URLField(max_length=50)
    quality = db.StringField(max_length=50)

class Radio(db.Document):
    name = db.StringField(max_length=50, required=True)
    frequencies = db.ListField(db.EmbeddedDocumentField(RadioFreq))
    streams = db.ListField(db.EmbeddedDocumentField(RadioStream))
    
# Shows

class ShowTime(db.EmbeddedDocument):
    hour = db.IntField(required=True)
    minute = db.IntField(required=True)

class ShowHost(db.EmbeddedDocument):
    name = db.StringField(max_length=50, required=True)
    description = db.StringField(max_length=50)
    photoUrl = db.URLField(max_length=50)

class Show(db.Document):
    name = db.StringField(max_length=50, required=True)
    description = db.StringField(max_length=50)
    day = db.StringField(max_length=50)
    startTime = db.EmbeddedDocumentField(ShowTime)
    endTime = db.EmbeddedDocumentField(ShowTime)
    photoUrl = db.URLField(max_length=50)
    hosts = db.ListField(db.EmbeddedDocumentField(ShowHost))
