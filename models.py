class RadioFrequency(object):
    location = basestring
    title = basestring

class RadioStream(object):
    url = basestring
    quality = basestring

class Radio(object):
    name = basestring
    frequencies = [RadioFrequency]
    streams = [RadioStream]
