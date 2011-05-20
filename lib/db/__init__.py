def simple_type(ty):
    return ty in [int, bool, basestring]

def check_simple_type(v, ty):
    if ty == bool:
        return type(v) == bool
    if ty == int:
        return type(v) == int
    return isinstance(v, ty)

def check_one_type(v, t):
    if isinstance(t, list) and len(t) == 1:
        t = t[0]
        if not isinstance(v, list):
            return False
        if len(v) == 0:
            return True
        for e in v:
            if not check_one_type(e, t):
                return False
        return True
    test = check_simple_type if simple_type(t) else check_model
    return test(v, t)

def check_model(d, model, allow_missing_members=False):
    if not isinstance(d, dict) or not isinstance(model, type):
        return False
    spec = [(n, v) for (n, v) in model.__dict__.iteritems()
            if not n.startswith("_")]
    if not allow_missing_members and len(d) != len(spec):
        return False
    for (n, t) in spec:
        try:
            if not check_one_type(d[n], t):
                return False
        except KeyError:
            if not allow_missing_members:
                return False
    return True
