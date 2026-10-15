import pytest

from websocket_test import build, inventory_uri, load_inventory, write_project


@pytest.mark.parametrize('jobs', [1, 2])
def test_routingtable_reference_on_clean_and_incremental_build(tmp_path, jobs):
    sources = {
        'index.rst': '''
            API
            ===

            .. toctree::

               routes
               references
        ''',
        'routes.rst': '''
            Routes
            ======

            .. http:get:: /health
        ''',
        'references.rst': '''
            References
            ==========

            :ref:`routingtable`

            :ref:`All routes <routingtable>`
        ''',
    }
    source = write_project(tmp_path, sources)
    for stage in ('clean', 'incremental', 'unchanged'):
        if stage == 'incremental':
            with (source / 'references.rst').open('a', encoding='utf-8') as page:
                page.write('\nUpdated reference: :ref:`routingtable`\n')
        result, output = build(source, tmp_path, jobs=jobs)
        assert result.returncode == 0, result.stdout + result.stderr
        page = (output / 'references.html').read_text(encoding='utf-8')
        assert 'href="http-routingtable.html"' in page
        assert 'HTTP Routing Table' in page
        assert 'All routes' in page
        assert (output / 'http-routingtable.html').exists()
        inventory = load_inventory(output)
        assert inventory_uri(inventory['std:label']['routingtable']) == 'http-routingtable.html'
