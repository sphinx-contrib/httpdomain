import hashlib
import os
import posixpath
import subprocess
import sys
import textwrap
import zipfile
from pathlib import Path

import pytest

from docutils import nodes
from sphinx import addnodes
from sphinx.util.inventory import InventoryFile

from sphinxcontrib.httpdomain._path_signature import render_path_signature
from sphinxcontrib.httpdomain.websocket import connection_anchor


def write_project(tmp_path, sources, language='en', toc_object_entries=True):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'conf.py').write_text(
        "extensions = ['sphinxcontrib.httpdomain']\n"
        "master_doc = 'index'\n"
        "project = 'WebSocket test project'\n"
        "html_theme = 'sphinxdoc'\n"
        "language = %r\n"
        "toc_object_entries = %r\n" % (language, toc_object_entries),
        encoding='utf-8',
    )
    for name, content in sources.items():
        (source / name).write_text(textwrap.dedent(content), encoding='utf-8')
    return source


def build(source, tmp_path, warning_is_error=True, jobs=1):
    output = tmp_path / 'html'
    doctrees = tmp_path / 'doctrees'
    command = [
        sys.executable,
        '-m',
        'sphinx',
        '-b',
        'html',
        '-j',
        str(jobs),
        '-d',
        str(doctrees),
    ]
    if warning_is_error:
        command.append('-W')
    command.extend((str(source), str(output)))
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return result, output


def load_inventory(output):
    with (output / 'objects.inv').open('rb') as inventory_file:
        return InventoryFile.load(inventory_file, '', posixpath.join)


def inventory_uri(item):
    return item.uri if hasattr(item, 'uri') else item[2]


def test_websocket_domain_builds_parallel_with_http(tmp_path):
    source = write_project(tmp_path, {
        'index.rst': """
            WebSocket API
            =============

            .. toctree::

               chat
               references

            :ref:`websocket-routingtable`
        """,
        'chat.rst': """
            Chat
            ====

            .. websocket:connection:: /chat/(str:room)
               :synopsis: Join a chat room.
               :deprecated:
               :addtoc:

               :param string room: room identifier
               :query string token: optional access token
               :server-message joined: confirms the connection
               :client-message send: sends a message
               :server-event legacy: ordinary field-list content
               :statuscode 200: ordinary field-list content

            .. websocket:connection:: /hidden
               :no-index:

               Rendered without a public object.

            .. http:get:: /chat/(str:room)

               HTTP and WebSocket paths can coexist.
        """,
        'references.rst': """
            References
            ==========

            :websocket:connection:`/chat/(str:room)`
            :websocket:connection:`Chat endpoint </chat/(str:room)>`
            :websocket:connection:`/hidden`
            :websocket:connection:`/missing`
        """,
    })

    result, output = build(source, tmp_path, jobs=2)
    assert result.returncode == 0, result.stdout + result.stderr

    chat = (output / 'chat.html').read_text(encoding='utf-8')
    references = (output / 'references.html').read_text(encoding='utf-8')
    index = (output / 'index.html').read_text(encoding='utf-8')
    anchor = connection_anchor('/chat/(str:room)')

    assert 'id="%s"' % anchor in chat
    assert 'Messages sent by server' in chat
    assert 'Messages sent by client' in chat
    assert '<strong>joined</strong>' in chat
    assert '<strong>send</strong>' in chat
    assert 'Server-event legacy' in chat
    assert 'Statuscode 200' in chat
    assert connection_anchor('/hidden') not in chat
    assert 'href="#%s"><code' % anchor in chat
    assert 'websocket-routingtable.html' in index
    assert references.count('href="chat.html#%s"' % anchor) == 2
    assert '/hidden</span>' in references
    assert '/missing</span>' in references

    inventory = load_inventory(output)
    assert set(inventory['websocket:connection']) == {'/chat/(str:room)'}
    assert inventory_uri(inventory['websocket:connection']['/chat/(str:room)']) == (
        'chat.html#%s' % anchor
    )
    assert 'http:get' in inventory


def test_path_rendering_and_websocket_anchor_contract():
    signode = addnodes.desc_signature('', '')
    assert render_path_signature('/chat/(str:room)', signode) == '/chat/'
    assert signode.astext() == '/chat/(str: , room)'

    anchor = connection_anchor('/chat/(str:room)')
    assert anchor == (
        'websocket-chat-str-room-'
        '55927ebde7fc06254259051223793533de891d3c6c36658294fccc57d9eb9779'
    )
    assert connection_anchor('/a/b') != connection_anchor('/a-b')
    unicode_signature = '🌐/(str:room)'
    expected_digest = hashlib.sha256(
        unicode_signature.encode('utf-8')
    ).hexdigest()
    assert connection_anchor(unicode_signature) == (
        'websocket-str-room-%s' % expected_digest
    )
    assert connection_anchor('///').startswith('websocket-connection-')


def test_http_path_rendering_regression(tmp_path):
    source = write_project(tmp_path, {
        'index.rst': """
            HTTP regression
            ===============

            .. http:get:: /health

            .. http:get:: /users/(int:user_id)

            :http:get:`/health`
            :http:get:`/users/(int:user_id)`
            :ref:`routingtable`
        """,
    })
    result, output = build(source, tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr

    page = (output / 'index.html').read_text(encoding='utf-8')
    assert 'id="get--health"' in page
    assert 'id="get--users-(int-user_id)"' in page
    assert 'GET /users/' in page
    assert 'routingtable.html' in page
    inventory = load_inventory(output)
    assert inventory_uri(inventory['http:get']['/health']) == 'index.html#get--health'
    assert inventory_uri(inventory['http:get']['/users/(int:user_id)']) == (
        'index.html#get--users-(int-user_id)'
    )


def test_invalid_websocket_input_warns_and_is_not_registered(tmp_path):
    source = write_project(tmp_path, {
        'index.rst': """
            Invalid input
            =============

            .. websocket:connection:: chat

            :websocket:connection:`chat`

            .. websocket:connection:: /duplicate

            .. websocket:connection:: /duplicate
        """,
    })
    result, output = build(source, tmp_path, warning_is_error=False)
    assert result.returncode == 0, result.stdout + result.stderr
    diagnostics = result.stdout + result.stderr
    assert diagnostics.count('WebSocket connection paths must begin with') == 1
    assert diagnostics.count('WebSocket connection targets must begin with') == 1
    assert diagnostics.count('duplicate WebSocket connection definition /duplicate') == 1
    assert 'Use :noindex: for an intentional secondary rendering.' in diagnostics
    assert 'index.rst.rst' not in diagnostics

    inventory = load_inventory(output)
    assert set(inventory['websocket:connection']) == {'/duplicate'}
    assert 'chat' not in inventory['websocket:connection']
    duplicate_anchor = connection_anchor('/duplicate')
    page = (output / 'index.html').read_text(encoding='utf-8')
    assert page.count('id="%s"' % duplicate_anchor) == 1


def test_french_catalog_is_loaded(tmp_path):
    source = write_project(tmp_path, {
        'index.rst': """
            Chat
            ====

            .. websocket:connection:: /chat

               :server-message joined: joined
               :client-message send: send
        """,
    }, language='fr_FR')
    result, output = build(source, tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    page = (output / 'index.html').read_text(encoding='utf-8')
    routing_table = (output / 'websocket-routingtable.html').read_text(
        encoding='utf-8'
    )
    assert 'Messages envoyés par le serveur' in page
    assert 'Messages envoyés par le client' in page
    assert 'Table de routage WebSocket' in routing_table


@pytest.mark.skipif(
    not os.environ.get('HTTPDOMAIN_WHEEL_SMOKE'),
    reason='wheel smoke runs in the py310 tox environment',
)
def test_wheel_includes_locale_catalogs(tmp_path):
    output = tmp_path / 'dist'
    result = subprocess.run(
        ['uv', 'build', '--wheel', '--out-dir', str(output)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    wheel = next(output.glob('*.whl'))
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    assert ('sphinxcontrib/httpdomain/locale/fr_FR/LC_MESSAGES/'
            'httpdomain.mo') in names
    assert ('sphinxcontrib/httpdomain/locale/es_ES/LC_MESSAGES/'
            'httpdomain.mo') in names
