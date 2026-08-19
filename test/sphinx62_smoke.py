"""Minimal Sphinx 6.2 compatibility smoke test for the WebSocket domain."""

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import sphinx


def main():
    assert sphinx.__version__ == '6.2.1', sphinx.__version__
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        source = root / 'source'
        output = root / 'html'
        doctrees = root / 'doctrees'
        source.mkdir()
        (source / 'conf.py').write_text(
            "extensions = ['sphinxcontrib.httpdomain']\n"
            "master_doc = 'index'\n"
            "project = 'Sphinx 6.2 smoke'\n",
            encoding='utf-8',
        )
        (source / 'index.rst').write_text(textwrap.dedent("""
            API
            ===

            .. websocket:connection:: /chat/(str:room)

               :server-message joined: connection confirmed

            .. websocket:connection:: /hidden
               :no-index:

            :websocket:connection:`/chat/(str:room)`
            :ref:`websocket-routingtable`

            .. http:get:: /users/(int:user_id)
        """), encoding='utf-8')
        result = subprocess.run(
            [
                sys.executable,
                '-m',
                'sphinx',
                '-W',
                '-b',
                'html',
                '-d',
                str(doctrees),
                str(source),
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        page = (output / 'index.html').read_text(encoding='utf-8')
        assert 'websocket-chat-str-room-' in page
        assert 'websocket-routingtable.html' in page
        assert 'get--users-(int-user_id)' in page


if __name__ == '__main__':
    main()
