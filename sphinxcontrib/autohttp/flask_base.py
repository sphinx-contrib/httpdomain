"""
    sphinxcontrib.autohttp.flask
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The sphinx.ext.autodoc-style HTTP API reference builder (from Flask)
    for sphinxcontrib.httpdomain.

    :copyright: Copyright 2011 by Hong Minhee
    :license: BSD, see LICENSE for details.

"""

import re
import itertools
import six

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList

from sphinx.util import force_decode
from sphinx.util.compat import Directive
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.docstrings import prepare_docstring
from sphinx.pycode import ModuleAnalyzer

from sphinxcontrib import httpdomain
from sphinxcontrib.autohttp.common import http_directive, import_object


def translate_werkzeug_rule(rule):
    from werkzeug.routing import parse_rule
    buf = six.StringIO()
    for conv, arg, var in parse_rule(rule):
        if conv:
            buf.write('(')
            if conv != 'default':
                buf.write(conv)
                buf.write(':')
            buf.write(var)
            buf.write(')')
        else:
            buf.write(var)
    return buf.getvalue()


def get_routes(app, endpoint=None):
    endpoints = []
    for rule in app.url_map.iter_rules(endpoint):
        if rule.endpoint not in endpoints:
            endpoints.append(rule.endpoint)
    for endpoint in endpoints:
        methodrules = {}
        for rule in app.url_map.iter_rules(endpoint):
            methods = rule.methods.difference(['OPTIONS', 'HEAD'])
            path = translate_werkzeug_rule(rule.rule)
            for method in methods:
                if method in methodrules:
                    methodrules[method].append(path)
                else:
                    methodrules[method] = [path]
        for method, paths in methodrules.items():
            yield method, paths, endpoint

def quickref_directive(method, path, content):
    rcomp = re.compile("^\s*.. :quickref:\s*(?P<quick>.*)$")
    method = method.lower().strip()
    if isinstance(content, six.string_types):
         content = content.splitlines()
    description=""
    name=""
    ref = path.replace("<","(").replace(">",")").replace("/","-").replace(":","-")
    for line in content:
         qref = rcomp.match(line)
         if qref:
            quickref = qref.group("quick")
            parts = quickref.split(";",1)
            if len(parts)>1:
                name = parts[0]
                description= parts[1]
            else:
                description= quickref
            break

    row ={}
    row['name'] = name
    row['operation'] = '      - `%s %s <#%s-%s>`_' % (method.upper(), path, method.lower(), ref)
    row['description'] = description

    return row

class AutoflaskBase(Directive):

    has_content = True
    required_arguments = 1
    option_spec = {'endpoints': directives.unchanged,
                   'blueprints': directives.unchanged,
                   'modules': directives.unchanged,
                   'undoc-endpoints': directives.unchanged,
                   'undoc-blueprints': directives.unchanged,
                   'undoc-modules': directives.unchanged,
                   'undoc-static': directives.unchanged,
                   'include-empty-docstring': directives.unchanged}

    @property
    def endpoints(self):
        endpoints = self.options.get('endpoints', None)
        if not endpoints:
            return None
        return re.split(r'\s*,\s*', endpoints)

    @property
    def undoc_endpoints(self):
        undoc_endpoints = self.options.get('undoc-endpoints', None)
        if not undoc_endpoints:
            return frozenset()
        return frozenset(re.split(r'\s*,\s*', undoc_endpoints))

    @property
    def blueprints(self):
        blueprints = self.options.get('blueprints', None)
        if not blueprints:
            return None
        return frozenset(re.split(r'\s*,\s*', blueprints))

    @property
    def undoc_blueprints(self):
        undoc_blueprints = self.options.get('undoc-blueprints', None)
        if not undoc_blueprints:
            return frozenset()
        return frozenset(re.split(r'\s*,\s*', undoc_blueprints))

    @property
    def modules(self):
        modules = self.options.get('modules', None)
        if not modules:
            return frozenset()
        return frozenset(re.split(r'\s*,\s*', modules))

    @property
    def undoc_modules(self):
        undoc_modules = self.options.get('undoc-modules', None)
        if not undoc_modules:
            return frozenset()
        return frozenset(re.split(r'\s*,\s*', undoc_modules))

    def make_rst(self, qref=False):
        app = import_object(self.arguments[0])
        if self.endpoints:
            routes = itertools.chain(*[get_routes(app, endpoint)
                    for endpoint in self.endpoints])
        else:
            routes = get_routes(app)
        for method, paths, endpoint in routes:
            try:
                blueprint, _, endpoint_internal = endpoint.rpartition('.')
                if self.blueprints and blueprint not in self.blueprints:
                    continue
                if blueprint in self.undoc_blueprints:
                    continue
            except ValueError:
                pass  # endpoint is not within a blueprint

            if endpoint in self.undoc_endpoints:
                continue
            try:
                static_url_path = app.static_url_path # Flask 0.7 or higher
            except AttributeError:
                static_url_path = app.static_path # Flask 0.6 or under
            if ('undoc-static' in self.options and endpoint == 'static' and
                static_url_path + '/(path:filename)' in paths):
                continue
            view = app.view_functions[endpoint]

            if self.modules and view.__module__ not in self.modules:
                continue

            if self.undoc_modules and view.__module__ in self.modules:
                continue

            docstring = view.__doc__ or ''
            if hasattr(view, 'view_class'):
                meth_func = getattr(view.view_class, method.lower(), None)
                if meth_func and meth_func.__doc__:
                    docstring = meth_func.__doc__
            if not isinstance(docstring, six.text_type):
                analyzer = ModuleAnalyzer.for_module(view.__module__)
                docstring = force_decode(docstring, analyzer.encoding)

            if not docstring and 'include-empty-docstring' not in self.options:
                continue
            docstring = prepare_docstring(docstring)
            if qref == True:
                for path in paths:
                    row = quickref_directive(method, path, docstring)
                    yield row
            else:
                for line in http_directive(method, paths, docstring):
                    yield line
