"""Test JSON fields."""
import subprocess
import sys
import textwrap

from pathlib import Path


def write_project(tmp_path, sources, language='en', toc_object_entries=True):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'conf.py').write_text(
        "extensions = ['sphinxcontrib.httpdomain']\n"
        "master_doc = 'index'\n"
        "project = 'JSON fields test project'\n"
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


def test_json_fields_build(tmp_path:Path) -> None:
    source = write_project(tmp_path, {
        "index.rst": """
        JSON fields
        ===========
        
        ..  http:get:: /users/(int:user_id)/posts/(int:post_id)
        
            :reqjson integer user_id: The user ID 1.
            :>json string post_id: The post ID 1.
        
        ..  http:get:: /users/(int:user_id)/posts/(int:post_id)
        
            :reqjson reqjsonobj user_id: The user ID 2.
            :>json >jsonobj post_id: The post ID 2.
        
        ..  http:get:: /users/(int:user_id)/posts/(int:post_id)
        
            :resjson boolean ok: Operation status 1.
            :<json integer error: Error code 1.
        
        ..  http:get:: /users/(int:user_id)/posts/(int:post_id)
        
            :resjson resjsonobj ok: Operation status 2.
            :<json <jsonobj error: Error code 2.
        
        ..  http:get:: /users/(int:user_id)/posts/(int:post_id)

            :reqjsonarr integer user_id: The user ID 1.
            :reqjsonarr reqjsonarrtype post_id: The post ID 1.
            :>jsonarr integer publish: Date published.
            :>jsonarr >jsonarrtype sticky: Whether the post is sticky.

        ..  http:get:: /users/(int:user_id)/posts/(int:post_id)
        
            :resjsonarr boolean ok: Operation status. Not present in case of error
            :resjsonarr resjsonarrtype id: Object ID
            :<jsonarr string error: Error type
            :<jsonarr <jsonarrtype reason: Error reason
        """
    })
    result, output = build(source, tmp_path, jobs=1)
    assert result.returncode == 0, result.stdout + result.stderr
    index = (output / "index.html").read_text(encoding="utf-8")
    print(index)
    assert "Request JSON Object" in index
    assert "<strong>user_id</strong> (<em>integer</em>) – The user ID 1." in index
    assert "<strong>post_id</strong> (<em>string</em>) – The post ID 1." in index

    assert "<strong>user_id</strong> (<em>reqjsonobj</em>) – The user ID 2." in index
    assert "<strong>post_id</strong> (<em>&gt;jsonobj</em>) – The post ID 2." in index

    assert "Response JSON Object" in index
    assert "<strong>ok</strong> (<em>boolean</em>) – Operation status 1." in index
    assert "<strong>error</strong> (<em>integer</em>) – Error code 1." in index

    assert "<strong>ok</strong> (<em>resjsonobj</em>) – Operation status 2." in index
    assert "<strong>error</strong> (<em>&lt;jsonobj</em>) – Error code 2." in index

    assert "Request JSON Array of Objects" in index
    assert "<strong>user_id</strong> (<em>integer</em>) – The user ID 1." in index
    assert "<strong>post_id</strong> (<em>reqjsonarrtype</em>) – The post ID 1." in index
    assert "<strong>publish</strong> (<em>integer</em>) – Date published." in index
    assert "<strong>sticky</strong> (<em>&gt;jsonarrtype</em>) – Whether the post is sticky." in index

    assert "Response JSON Array of Objects" in index
    assert "<strong>ok</strong> (<em>boolean</em>) – Operation status. Not present in case of error" in index
    assert "<strong>id</strong> (<em>resjsonarrtype</em>) – Object ID" in index
    assert "<strong>error</strong> (<em>string</em>) – Error type" in index
    assert "<strong>reason</strong> (<em>&lt;jsonarrtype</em>) – Error reason" in index
