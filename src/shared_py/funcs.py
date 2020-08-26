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
