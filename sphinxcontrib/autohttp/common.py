"""
    sphinxcontrib.autohttp.common
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The common functions for web framework reflection.

    :copyright: Copyright 2011 by Hong Minhee
    :license: BSD, see LICENSE for details.

"""
# Python 3 Change
# __builtin__ in Py3 is renamed to builtins
# see: http://docs.pythonsprints.com/python3_porting/py-porting.html#name-changes
PY_VER = 2
try:
    import builtins
    import functools
    PY_VER = 3 
except ImportError:
    import __builtin__ 

def import_object(import_name):
    module_name, expr = import_name.split(':', 1)
    mod = __import__(module_name)
    if PY_VER == 2:
        mod = reduce(getattr, module_name.split('.')[1:], mod)
        globals = __builtin__
    else:
        mod = functools.reduce(getattr, module_name.split('.')[1:], mod)
        globals = builtins
    if not isinstance(globals, dict):
        globals = globals.__dict__
    return eval(expr, globals, mod.__dict__)


def http_directive(method, path, content):
    method = method.lower().strip()
    if PY_VER == 2:
        if isinstance(content, basestring):
            content = content.splitlines()
    else:
        if isinstance(content, str):
            content = content.splitlines()   
    yield ''
    yield '.. http:{method}:: {path}'.format(**locals())
    yield ''
    for line in content:
        yield '   ' + line
    yield ''
