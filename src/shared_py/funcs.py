import sys
# shared functions

def get_the_only_element(l):
    if len(l) > 1:
        raise RuntimeError("matched more than one element!\n", l)
    elif len(l) == 0:
        raise RuntimeError("matched none element!\n", l)
    else:
        return l[0]

def eprint(msg):
    print(msg, file=sys.stderr)

def return_none_if_no_key(e, l):
    first = l[0]
    rest = l[1:]
    if e is None:
        return None
    elif first not in e:
        return None
    elif len(l) == 1:
        return e[first]
    else:
        return return_none_if_no_key(e[first], rest)
