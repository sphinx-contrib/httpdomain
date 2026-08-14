import pathlib
import tempfile
import unittest

from sphinx import addnodes
from sphinx.application import Sphinx


class NoindexTestCase(unittest.TestCase):
    """The noindex option must skip only the global route registration.

    The per-page anchor on the signature (and with it the HTML permalink)
    must survive, so pages that document a route already indexed by another
    page keep working deep links.
    """

    def build(self):
        self.tmp = tempfile.TemporaryDirectory()
        src = pathlib.Path(self.tmp.name, 'src')
        src.mkdir()
        (src / 'conf.py').write_text(
            "extensions = ['sphinxcontrib.httpdomain']\n"
        )
        (src / 'index.rst').write_text(
            'Index\n'
            '=====\n'
            '\n'
            '.. toctree::\n'
            '\n'
            '   other\n'
            '\n'
            '.. http:post:: /demo\n'
            '\n'
            '   Canonical description.\n'
        )
        (src / 'other.rst').write_text(
            'Other\n'
            '=====\n'
            '\n'
            '.. http:post:: /demo\n'
            '   :noindex:\n'
            '\n'
            '   Alternative description of the same route.\n'
        )
        out = pathlib.Path(self.tmp.name, 'out')
        app = Sphinx(
            str(src), str(src), str(out), str(out / '.doctrees'), 'html',
            status=None,
        )
        app.build()
        return app

    def tearDown(self):
        self.tmp.cleanup()

    def test_noindex_skips_registration(self):
        app = self.build()
        entries = app.env.domaindata['http']['post']
        self.assertIn('/demo', entries)
        self.assertEqual(entries['/demo'][0], 'index')

    def test_noindex_keeps_anchor(self):
        app = self.build()
        doctree = app.env.get_doctree('other')
        ids = [
            anchor
            for node in doctree.findall(addnodes.desc_signature)
            for anchor in node['ids']
        ]
        self.assertEqual(ids, ['post--demo'])
