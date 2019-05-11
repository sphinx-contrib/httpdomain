"""
    sphinxcontrib.autohttp.drf
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The sphinx.ext.autodoc-style HTTP API reference builder (from DRF)
    for sphinxcontrib.httpdomain.

    :copyright: Copyright 2013 by Rodrigo Machado
    :license: BSD, see LICENSE for details.

"""

import inspect
import re
from itertools import chain

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import ViewList

from sphinx.util.nodes import nested_parse_with_titles
from sphinxcontrib.autohttp.common import http_directive


def chain_routes(schema):
    if schema.data:
        yield from chain(*map(lambda x: chain_routes(x), schema.data.values()))
    elif schema.links:
        yield from schema.links.values()


def get_routes(urlconf=None):
    from rest_framework.schemas import SchemaGenerator
    generator = SchemaGenerator(
        title=None, url=None, description=None,
        urlconf=urlconf, patterns=None,
    )
    yield from chain_routes(generator.get_schema())


def get_schema_type(schema):
    return {
        'Integer': 'int',
        'Number': 'int',
        'String': 'str',
        'Enum': 'choice',
    }.get(schema.__class__.__name__)


class AutoDRFDirective(Directive):

    has_content = True
    required_arguments = 0
    option_spec = {
        'urlconf': directives.unchanged,
    }

    @property
    def urlconf(self):
        urlconf = self.options.get('urlconf', None)
        if not urlconf:
            return None
        return urlconf

    def make_rst(self):
        for link in get_routes(self.urlconf):
            for line in http_directive(link.action, link.url, link.description):
                yield line
            for field in link.fields:
                line = '   :{} '.format({'form': '<json', 'query': 'query', 'path': 'param'}[field.location])
                type_ = get_schema_type(field.schema)
                if type_:
                    line += '{} '.format(type_)
                line += '{}: {}'.format(field.name, field.description or field.schema.description)
                if type_ == 'choice' and len(field.schema.enum) < 30:
                    line += ' **Choices:** {}'.format(', '.join(map(lambda x: '*"{}"*'.format(x), field.schema.enum)))
                yield line


    def run(self):
        node = nodes.section()
        node.document = self.state.document
        result = ViewList()
        for line in self.make_rst():
            result.append(line, '<autodrf>')
        nested_parse_with_titles(self.state, result, node)
        return node.children


def setup(app):
    app.setup_extension('sphinxcontrib.httpdomain')
    app.add_directive('autodrf', AutoDRFDirective)
