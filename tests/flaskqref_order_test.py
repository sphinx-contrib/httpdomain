import pickle
import subprocess
import sys

import pytest

from docutils import nodes
from sphinx import addnodes


@pytest.mark.parametrize('order', [None, 'path'])
@pytest.mark.parametrize('shared_resource', ['Root', ''])
def test_quick_reference_respects_order(tmp_path, order, shared_resource):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'conf.py').write_text(
        "import sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, str(Path(__file__).parent))\n"
        "extensions = ['sphinxcontrib.autohttp.flask', "
        "'sphinxcontrib.autohttp.flaskqref']\n"
        "project = 'Quick reference ordering'\n"
        "master_doc = 'index'\n",
        encoding='utf-8',
    )
    # Registration order, resource-name order and path order all differ.
    # The shared resource occurs on both sides of another resource in path
    # order, so preserving only the first resource occurrence is insufficient.
    (source / 'sampleapp.py').write_text(
        "from flask import Flask\n"
        "app = Flask(__name__, static_folder=None)\n"
        "specs = [('/z', %r), ('/b', 'Accounts'), "
        "('/a', %r), ('/c', %r)]\n"
        "for i, (path, resource) in enumerate(specs):\n"
        "    def view():\n"
        "        return ''\n"
        "    description = 'Shared description' if resource != 'Accounts' else 'Account description'\n"
        "    view.__doc__ = '.. :quickref: ' + resource + ';' + description\n"
        "    app.add_url_rule(path, 'endpoint' + str(i), view)\n"
        % (shared_resource, shared_resource, shared_resource),
        encoding='utf-8',
    )
    option = '   :order: path\n' if order == 'path' else ''
    (source / 'index.rst').write_text(
        'API\n===\n\n.. qrefflask:: sampleapp:app\n' + option +
        '\n.. autoflask:: sampleapp:app\n' + option,
        encoding='utf-8',
    )
    doctrees = tmp_path / 'doctrees'
    output = tmp_path / 'html'
    result = subprocess.run(
        [sys.executable, '-m', 'sphinx', '-W', '-b', 'html',
         '-d', str(doctrees), str(source), str(output)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    # This is the trusted doctree produced by the build just run above.
    with (doctrees / 'index.doctree').open('rb') as stream:
        document = pickle.load(stream)
    table = next(document.findall(nodes.table))
    body = next(table.findall(nodes.tbody))
    rows = [[entry.astext() for entry in row.children] for row in body.children]
    paths = [row[1].split()[1] for row in rows]
    details = [sig.astext().split()[1]
               for sig in document.findall(addnodes.desc_signature)]

    if order == 'path':
        assert paths == ['/a', '/b', '/c', '/z']
        assert paths == details
        assert [row[0] for row in rows] == [shared_resource, 'Accounts', shared_resource, '']
        assert [row[2] for row in rows] == [
            'Shared description', 'Account description', 'Shared description', '',
        ]
    else:
        assert details == ['/z', '/b', '/a', '/c']
        if shared_resource:
            assert paths == ['/b', '/z', '/a', '/c']
            assert [row[0] for row in rows] == ['Accounts', shared_resource, '', '']
            assert [row[2] for row in rows] == ['Account description', 'Shared description', '', '']
        else:
            assert paths == ['/z', '/a', '/c', '/b']
            assert [row[0] for row in rows] == ['', '', '', 'Accounts']
            assert [row[2] for row in rows] == ['Shared description', '', '', 'Account description']
