"""Shared rendering for HTTP and WebSocket path signatures."""

import re

from sphinx import addnodes


path_signature_param_re = re.compile(
    r'\((?:(?P<type>[^:)]+):)?(?P<name>[\w_]+)\)', re.VERBOSE
)


def render_path_signature(sig, signode):
    """Render typed path parameters into *signode* and return the final path part.

    The return value intentionally mirrors the historical HTTP implementation.
    """
    offset = 0
    path = None
    for match in path_signature_param_re.finditer(sig):
        path = sig[offset:match.start()]
        signode += addnodes.desc_name(path, path)
        params = addnodes.desc_parameterlist()
        typ = match.group('type')
        if typ:
            typ += ': '
            params += addnodes.desc_annotation(typ, typ)
        name = match.group('name')
        params += addnodes.desc_parameter(name, name)
        signode += params
        offset = match.end()
    if offset < len(sig):
        path = sig[offset:len(sig)]
        signode += addnodes.desc_name(path, path)
    assert path is not None, 'no matches for sig: %s' % sig
    return path
