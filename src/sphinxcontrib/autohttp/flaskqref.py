"""
    sphinxcontrib.autohttp.flaskqref
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The sphinx.ext.autodoc-style HTTP API quick reference
    builder (from Flask)
    for sphinxcontrib.httpdomain.

    :copyright: Copyright 2011 by Hong Minhee
    :license: BSD, see LICENSE for details.

"""

from itertools import groupby

from docutils import nodes
from docutils.statemachine import ViewList

from sphinxcontrib import httpdomain
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.locale import get_translation

from .flask import AutoflaskBase

_ = get_translation('httpdomain')


class QuickReferenceFlaskDirective(AutoflaskBase):


    header = [ '',
              '.. list-table::',
              '    :widths: 20 45 35',
              '    :header-rows: 1',
              '',
              '    * - ' + _('Resource'),
              '      - ' + _('Operation'),
              '      - ' + _('Description')
            ]

    def run(self):
        node = nodes.section()
        node.document = self.state.document
        result = ViewList()
        for line in QuickReferenceFlaskDirective.header:
            result.append(line, '<qrefflask>')
        rows = list(self.make_rst(qref=True))
        if self.order != 'path':
            # Keep the historical resource grouping unless endpoint order was
            # requested. The base directive already supplies path order.
            rows.sort(key=lambda row: row['name'])

        for name, resource_rows in groupby(rows, key=lambda row: row['name']):
            # Keep table display clean by not repeating duplicate
            # resource names and descriptions
            display_name = name
            previous_description=None
            for row in resource_rows:
                result.append('    * - %s' % display_name, '<qrefflask>')
                display_name =""
                result.append(row['operation'], '<qrefflask>')
                description = row['description']
                if previous_description is not None and previous_description == description:
                    description =""
                else:
                    previous_description = description

                result.append('      - %s' % description,  '<qrefflask>')

        result.append('', '<qrefflask>')
        nested_parse_with_titles(self.state, result, node)
        return node.children

def setup(app):
    app.setup_extension('sphinxcontrib.httpdomain')
    app.add_directive('qrefflask', QuickReferenceFlaskDirective)
