"""
    sphinxcontrib.autohttp.drf
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The sphinx.ext.autodoc-style HTTP API reference builder (from DRF)
    for sphinxcontrib.httpdomain.

    :copyright: Copyright 2013 by Rodrigo Machado
    :license: BSD, see LICENSE for details.

"""

from itertools import chain

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import ViewList

from sphinx.util.nodes import nested_parse_with_titles
from sphinxcontrib.autohttp.common import http_directive


LEVELS = [
    '#',
    '*',
    '=',
    '-',
    '^',
    '"',
]


def chain_routes(schema):
    if schema.data:
        yield from chain(*map(lambda x: chain_routes(x), schema.data.values()))
    elif schema.links:
        yield from schema.links.values()


def get_routes(urlconf=None, modules=None):
    generator = get_schema_generator_class()(
        title=None, url=None, description=None,
        urlconf=urlconf, patterns=None, modules=modules,
    )
    return generator.get_schema()


# def get_modules(modules=None):
#     from django.utils.module_loading import import_string
#     return [import_string(module) for module in map(lambda x: x.strip(), modules.split(','))]


def get_schema_type(schema):
    return {
        'Integer': 'int',
        'Number': 'int',
        'String': 'str',
        'Enum': 'choice',
    }.get(schema.__class__.__name__)


def issubmodule(cls, modules):
    modules = list(map(lambda x: '{}.'.format(x), modules))
    mod = cls.__module__
    return bool(next(filter(lambda x: mod.startswith(x), modules), None))


def get_schema_generator_class():
    from rest_framework.schemas.generators import EndpointEnumerator
    from rest_framework.schemas import SchemaGenerator

    class HttpDomainEndpointEnumerator(EndpointEnumerator):
        modules = None

        def get_api_endpoints(self, patterns=None, prefix=''):
            endpoints = super(HttpDomainEndpointEnumerator, self).get_api_endpoints(patterns, prefix)
            endpoints = map(lambda x: x, endpoints)
            if self.modules:
                endpoints = list(filter(lambda x: issubmodule(x[2].cls, self.modules), endpoints))
            return endpoints


    class HttpDomainSchemaGenerator(SchemaGenerator):
        def __init__(self, title=None, url=None, description=None, patterns=None, urlconf=None, modules=None):
            super(HttpDomainSchemaGenerator, self).__init__(title, url, description, patterns, urlconf)
            self.modules = modules

        @property
        def endpoint_inspector_cls(self):
            """Create a new class with the modules attribute. There is no possibility to put
            the argument when starting the instance
            """
            class EndpointEnumerator(HttpDomainEndpointEnumerator):
                modules = self.modules
            return EndpointEnumerator

        def _get_paths_and_endpoints(self, request):
            """Add ``swagger_fake_view`` to every api view.
            """
            paths, view_endpoints = super()._get_paths_and_endpoints(request)
            for view_endpoint in view_endpoints:
                path, method, view = view_endpoint
                setattr(view, 'swagger_fake_view', True)
            return paths, view_endpoints

    return HttpDomainSchemaGenerator


class AutoDRFDirective(Directive):

    has_content = True
    required_arguments = 0
    option_spec = {
        'urlconf': directives.unchanged,
        'modules': directives.unchanged,
        'titles': directives.unchanged,
    }

    @property
    def urlconf(self):
        urlconf = self.options.get('urlconf', None)
        if not urlconf:
            return None
        return urlconf

    @property
    def modules(self):
        return self.options.get('modules', None) or None

    @property
    def titles(self):
        titles = self.options.get('titles', None)
        if titles:
            return int(titles.strip())

    def make_rst(self):
        if self.modules:
            modules = [module.strip() for module in self.modules.split(',')]
        else:
            modules = []
        schema = get_routes(self.urlconf, modules)
        yield from self.get_schema_lines(schema, self.titles)
        # if self.modules:
        #     links =

    def get_schema_lines(self, schema, titles_level):
        # Generate the links of the actual level.
        if schema.links:
            for link_name, link in schema.links.items():
                yield from self.get_link_lines(link_name, link)
        # Visit recursively others levels and generate links if exists.
        if schema.data:
            for title, sub_schema in schema.data.items():
                if titles_level:
                    yield ''
                    yield title.title().replace('_', ' ')
                    yield LEVELS[(titles_level + 1) % len(LEVELS)] * len(title)
                    yield ''
                yield from self.get_schema_lines(sub_schema, (titles_level + 1) if titles_level else None)
            # yield from chain(*map(lambda x: chain_routes(x), schema.data.values()))

    def get_link_lines(self, link_name, link):
        for line in http_directive(link.action, link.url, link.description):
            yield line
        for field in link.fields:
            if link_name != 'list' and field.location == 'query':
                # Ignore query params in PUT/PATCH/etc.
                continue
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
