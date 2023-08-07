"""
This contains a global functions.
"""

def SET_GLOBALS():
    import builtins

    builtins.fly_dd = fly_pdb
    builtins.fly_print = fly_print

def fly_pdb():
    import pdb; pdb.set_trace()

def fly_print(*args):
    line = "-" * 30
    print(line)
    print('DEBUG')
    print(line)
    print(*args)
    print(line)

