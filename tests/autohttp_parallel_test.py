import os
import posixpath
import subprocess
import sys
import textwrap

import pytest

from sphinx.util.inventory import InventoryFile
from sphinx.util.parallel import parallel_available


APP_SOURCE = '''
from bottle import Bottle
from flask import Flask
from tornado.web import Application, RequestHandler


def make_app(framework, name):
    def view():
        return name
    view.__doc__ = "Description for " + name + "."
    path = "/" + name
    if framework == "bottle":
        app = Bottle()
        app.get(path, callback=view)
    elif framework == "tornado":
        handler = type(name, (RequestHandler,), {"get": view})
        app = Application([(path, handler)])
    else:
        app = Flask(name, static_folder=None)
        app.add_url_rule(path, name, view)
    return app


apps = {
    (framework, name): make_app(framework, name)
    for framework in ("bottle", "flask", "tornado")
    for name in ("first", "second", "third", "fourth", "fifth", "sixth")
}
'''


def build(source, output, jobs):
    result = subprocess.run(
        [sys.executable, '-m', 'sphinx', '-W', '-b', 'html', '-j', str(jobs),
         '-d', str(output / '.doctrees'), str(source), str(output)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'WARNING' not in result.stderr, result.stderr
    assert 'doing serial read' not in result.stdout + result.stderr


def http_inventory(output):
    with (output / 'objects.inv').open('rb') as stream:
        inventory = InventoryFile.load(stream, '', posixpath.join)
    return {
        path: item.uri if hasattr(item, 'uri') else item[2]
        for path, item in inventory['http:get'].items()
    }


@pytest.mark.parametrize('framework', ['bottle', 'flask', 'flaskqref', 'tornado'])
def test_autohttp_parallel_reading_preserves_routes(tmp_path, framework):
    source = tmp_path / 'source'
    source.mkdir()
    extensions = ['sphinxcontrib.autohttp.' + framework]
    if framework == 'flaskqref':
        extensions.insert(0, 'sphinxcontrib.autohttp.flask')
    (source / 'conf.py').write_text(textwrap.dedent('''
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        extensions = %r
        project = 'autohttp parallel test'
        master_doc = 'index'
        html_theme = 'sphinxdoc'

        def record_merge(app, env, docnames, other):
            with (Path(app.outdir) / 'workers.txt').open('a') as stream:
                stream.write(','.join(sorted(docnames)) + '\\n')

        def setup(app):
            for name in extensions:
                assert app.extensions[name].parallel_read_safe, name
            app.connect('env-merge-info', record_merge)
    ''') % extensions, encoding='utf-8')
    (source / 'sampleapp.py').write_text(APP_SOURCE, encoding='utf-8')
    names = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']
    (source / 'index.rst').write_text(
        'Index\n=====\n\n.. toctree::\n\n' +
        ''.join('   %s\n' % name for name in names), encoding='utf-8',
    )
    app_framework = 'flask' if framework == 'flaskqref' else framework
    directive = 'autoflask' if framework == 'flaskqref' else 'auto' + framework
    for name in names:
        target = "sampleapp:apps[%r,%r]" % (app_framework, name)
        content = '%s\n%s\n\n.. %s:: %s\n' % (
            name, '=' * len(name), directive, target,
        )
        if framework == 'flaskqref':
            content += '\n.. qrefflask:: %s\n   :autoquickref:\n' % target
        (source / (name + '.rst')).write_text(content, encoding='utf-8')

    serial = tmp_path / 'serial'
    parallel = tmp_path / 'parallel'
    build(source, serial, jobs=1)
    build(source, parallel, jobs=2)

    # Sphinx cannot fork readers on Windows. Linux must really merge worker
    # environments; accepting an unnoticed serial fallback would miss the bug.
    if parallel_available:
        workers = (parallel / 'workers.txt').read_text().splitlines()
        assert len(workers) >= 2
        assert set(','.join(workers).split(',')) >= set(names)
    expected = {'/' + name for name in names}
    assert set(http_inventory(parallel)) == expected
    assert http_inventory(parallel) == http_inventory(serial)
    for name in names:
        html = (parallel / (name + '.html')).read_text(encoding='utf-8')
        assert 'Description for %s.' % name in html
        assert 'id="get--%s"' % name in html
        if framework == 'flaskqref':
            assert 'href="#get--%s"' % name in html

    # Reread one document without its directive: stale worker-owned routes
    # must be purged, while the untouched documents keep their routes.
    changed = source / 'first.rst'
    changed.write_text('First\n=====\n\nRemoved route.\n', encoding='utf-8')
    stat = changed.stat()
    os.utime(changed, (stat.st_atime + 2, stat.st_mtime + 2))
    build(source, parallel, jobs=2)
    assert set(http_inventory(parallel)) == expected - {'/first'}
