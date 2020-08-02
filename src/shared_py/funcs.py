# shared functions

def get_the_only_element(l):
    if len(l) != 1:
        raise RuntimeError("matched more than one element!\n", l)
    else:
        return l[0]
