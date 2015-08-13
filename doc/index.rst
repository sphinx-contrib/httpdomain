.. sphinxcontrib-httpdomain documentation master file, created by
   sphinx-quickstart on Thu Jun  2 13:27:52 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. module:: sphinxcontrib.httpdomain

:mod:`sphinxcontrib.httpdomain` --- Documenting RESTful HTTP APIs
=================================================================

This contrib extension, :mod:`sphinxcontrib.httpdomain`, provides a Sphinx
domain for describing RESTful HTTP APIs.

.. seealso::

   We might support reflection for web framework your webapp depends on.
   See the following :mod:`sphinxcontrib.auttohttp` modules:

   Module :mod:`sphinxcontrib.autohttp.flask`
      Reflection for Flask_ webapps.

   Module :mod:`sphinxcontrib.autohttp.bottle`
      Reflection for Bottle_ webapps.

   Module :mod:`sphinxcontrib.autohttp.tornado`
      Reflection for Tornado_ webapps.


In order to use it, add :mod:`sphinxcontrib.httpdomain` into
:data:`extensions` list of your Sphinx configuration file (:file:`conf.py`)::

    extensions = ['sphinxcontrib.httpdomain']


Additional Configuration
------------------------

``http_headers_ignore_prefixes``
   List of HTTP header prefixes which should be ignored in strict mode::

       http_headers_ignore_prefixes = ['X-']

   .. versionadded:: 1.4.0

``http_index_ignore_prefixes``
   Strips the leading segments from the endpoint paths by given list
   of prefixes::

       http_index_ignore_prefixes = ['/internal', '/_proxy']

   .. versionadded:: 1.3.0

``http_index_shortname``
   Short name of the index which will appears on every page::

       http_index_shortname = 'api'

   .. versionadded:: 1.3.0

``http_index_localname``
   Full index name which is used on index page::

       http_index_localname = "My Project HTTP API"

   .. versionadded:: 1.3.0

``http_strict_mode``
   When ``True`` (default) emits build errors when status codes, methods and
   headers are looks non-standard::

       http_strict_mode = True

   .. versionadded:: 1.4.0


Basic usage
-----------

There are several provided :ref:`directives <directives>` that describe
HTTP resources.

.. sourcecode:: rst

   .. http:get:: /users/(int:user_id)/posts/(tag)

      The posts tagged with `tag` that the user (`user_id`) wrote.

      **Example request**:

      .. sourcecode:: http

         GET /users/123/posts/web HTTP/1.1
         Host: example.com
         Accept: application/json, text/javascript

      **Example response**:

      .. sourcecode:: http

         HTTP/1.1 200 OK
         Vary: Accept
         Content-Type: text/javascript

         [
           {
             "post_id": 12345,
             "author_id": 123,
             "tags": ["server", "web"],
             "subject": "I tried Nginx"
           },
           {
             "post_id": 12346,
             "author_id": 123,
             "tags": ["html5", "standards", "web"],
             "subject": "We go to HTML 5"
           }
         ]

      :query sort: one of ``hit``, ``created-at``
      :query offset: offset number. default is 0
      :query limit: limit number. default is 30
      :reqheader Accept: the response content type depends on
                         :mailheader:`Accept` header
      :reqheader Authorization: optional OAuth token to authenticate
      :resheader Content-Type: this depends on :mailheader:`Accept`
                               header of request
      :statuscode 200: no error
      :statuscode 404: there's no user

will be rendered as:

    .. http:get:: /users/(int:user_id)/posts/(tag)

       The posts tagged with `tag` that the user (`user_id`) wrote.

       **Example request**:

       .. sourcecode:: http

          GET /users/123/posts/web HTTP/1.1
          Host: example.com
          Accept: application/json, text/javascript

       **Example response**:

       .. sourcecode:: http

          HTTP/1.1 200 OK
          Vary: Accept
          Content-Type: text/javascript

          [
            {
              "post_id": 12345,
              "author_id": 123,
              "tags": ["server", "web"],
              "subject": "I tried Nginx"
            },
            {
              "post_id": 12346,
              "author_id": 123,
              "tags": ["html5", "standards", "web"],
              "subject": "We go to HTML 5"
            }
          ]

       :query sort: one of ``hit``, ``created-at``
       :query offset: offset number. default is 0
       :query limit: limit number. default is 30
       :reqheader Accept: the response content type depends on
                          :mailheader:`Accept` header
       :reqheader Authorization: optional OAuth token to authenticate
       :resheader Content-Type: this depends on :mailheader:`Accept`
                                header of request
       :statuscode 200: no error
       :statuscode 404: there's no user

Of course, :ref:`roles <roles>` that refer the directives as well.
For example:

.. sourcecode:: rst

   :http:get:`/users/(int:user_id)/posts/(tag)`

will render like:

    :http:get:`/users/(int:user_id)/posts/(tag)`


.. _directives:

Directives
----------

.. rst:directive:: .. http:options:: path

   Describes a HTTP resource's :http:method:`OPTIONS` method.
   It can also be referred by :rst:role:`http:options` role.

.. rst:directive:: .. http:head:: path

   Describes a HTTP resource's :http:method:`HEAD` method.
   It can also be referred by :rst:role:`http:head` role.

.. rst:directive:: .. http:post:: path

   Describes a HTTP resource's :http:method:`POST` method.
   It can also be referred by :rst:role:`http:post` role.

.. rst:directive:: .. http:get:: path

   Describes a HTTP resource's :http:method:`GET` method.
   It can also be referred by :rst:role:`http:get` role.

.. rst:directive:: .. http:put:: path

   Describes a HTTP resource's :http:method:`PUT` method.
   It can also be referred by :rst:role:`http:put` role.

.. rst:directive:: .. http:patch:: path

   Describes a HTTP resource's :http:method:`PATCH` method.
   It can also be referred by :rst:role:`http:patch` role.

.. rst:directive:: .. http:delete:: path

   Describes a HTTP resource's :http:method:`DELETE` method.
   It can also be referred by :rst:role:`http:delete` role.

.. rst:directive:: .. http:trace:: path

   Describes a HTTP resource's :http:method:`TRACE` method.
   It can also be referred by :rst:role:`http:trace` role.

.. rst:directive:: .. http:copy:: path

   Describes a HTTP resource's :http:method:`COPY` method.
   It can also be referred by :rst:role:`http:copy` role.

   .. versionadded:: 1.3.0

.. rst:directive:: .. http:any:: path

   Describes a HTTP resource's which accepts requests with
   :http:method:`ANY` method. Useful for cases when requested resource
   proxying the request to some other location keeping original request
   context. It can also be referred by :rst:role:`http:any` role.

   .. versionadded:: 1.3.0


Options
```````

.. versionadded:: 1.3.0

Additionally, you may specify custom options to the directives:

``noindex``
   Excludes specific directive from HTTP routing table.

   .. sourcecode:: rst

      .. http:get:: /users/(int:user_id)/posts/(tag)
         :noindex:

``deprecated``
   Marks the method as deprecated in HTTP routing table.

   .. sourcecode:: rst

      .. http:get:: /users/(int:user_id)/tagged_posts
         :deprecated:

``synopsis``
   Adds short description for HTTP routing table.

   .. sourcecode:: rst

      .. http:get:: /users/(int:user_id)/posts/(tag)
         :synopsis: Returns posts by the specified tag for the user


.. _resource-fields:

Resource Fields
---------------

Inside HTTP resource description directives like :rst:dir:`get`,
reStructuredText field lists with these fields are recognized and formatted
nicely:

``param``, ``parameter``, ``arg``, ``argument``
   Description of URL parameter.

``queryparameter``, ``queryparam``, ``qparam``, ``query``
   Description of parameter passed by request query string.

   It optionally can be typed, all the query parameters will have obviously
   string types though.  But it's useful if there's conventions for it.

   .. versionchanged:: 1.1.9

      It can be typed e.g.:

      .. sourcecode:: rst

         :query string title: the post title
         :query string body: the post body
         :query boolean sticky: whether it's sticky or not

``formparameter``, ``formparam``, ``fparam``, ``form``
   Description of parameter passed by request content body, encoded in
   :mimetype:`application/x-www-form-urlencoded` or
   :mimetype:`multipart/form-data`.

``jsonparameter``, ``jsonparam``, ``json``
   Description of a parameter passed by request content body, encoded in
   :mimetype:`application/json`.

   .. deprecated:: 1.3.0
      Use ``reqjsonobj``/``reqjson``/``<jsonobj``/``<json`` and
      ``reqjsonarr``/``<jsonarr`` instead.

   .. versionadded:: 1.1.8

   .. versionchanged:: 1.1.9

      It can be typed e.g.:

      .. sourcecode:: rst

         :jsonparam string title: the post title
         :jsonparam string body: the post body
         :jsonparam boolean sticky: whether it's sticky or not

``reqjsonobj``, ``reqjson``, ``<jsonobj``, ``<json``
   Description of a single field of JSON object passed by request body,
   encoded in :mimetype:`application/json`. The key difference from ``json`` is
   explicitly defined use-case (request/response) of the described object.

   .. sourcecode:: rst

      :<json string title: the post title
      :<json string body: the post body
      :<json boolean sticky: whether it's sticky or not

   .. versionadded:: 1.3.0

``resjsonobj``, ``resjson``, ``>jsonobj``, ``>json``
   Description of a single field of JSON object returned with response body,
   encoded in :mimetype:`application/json`.

   .. sourcecode:: rst

      :>json boolean ok: Operation status

   .. versionadded:: 1.3.0

``reqjsonarr``, ``<jsonarr``
``resjsonarr``, ``>jsonarr``

   Similar to ``<json`` and ``>json`` respectively, but uses for describing
   objects schema inside of returned array.

   Let's say, the response contains the following data:

   .. sourcecode:: javascript

      [{"id": "foo", "ok": true}, {"id": "bar", "error": "forbidden", "reason": "sorry"}]

   Then we can describe it in the following way:

   .. sourcecode:: rst

      :>jsonarr boolean ok: Operation status. Not present in case of error
      :>jsonarr string id: Object ID
      :>jsonarr string error: Error type
      :>jsonarr string reason: Error reason

   .. versionadded:: 1.3.0

.. sourcecode:: rst

      :>json boolean status: Operation status

``requestheader``, ``reqheader``, ``>header``
   Description of request header field.

   .. versionadded:: 1.1.9

``responseheader``, ``resheader``, ``<header``
   Description of response header field.

   .. versionadded:: 1.1.9

``statuscode``, ``status``, ``code``
   Description of response status code.

For example:

.. sourcecode:: rst

   .. http:post:: /posts/(int:post_id)

      Replies a comment to the post.

      :param post_id: post's unique id
      :type post_id: int
      :form email: author email address
      :form body: comment body
      :reqheader Accept: the response content type depends on
                         :mailheader:`Accept` header
      :reqheader Authorization: optional OAuth token to authenticate
      :resheader Content-Type: this depends on :mailheader:`Accept`
                               header of request
      :status 302: and then redirects to :http:get:`/posts/(int:post_id)`
      :status 400: when form parameters are missing

It will render like this:

    .. http:post:: /posts/(int:post_id)

       Replies a comment to the post.

       :param post_id: post's unique id
       :type post_id: int
       :form email: author email address
       :form body: comment body
       :reqheader Accept: the response content type depends on
                          :mailheader:`Accept` header
       :reqheader Authorization: optional OAuth token to authenticate
       :resheader Content-Type: this depends on :mailheader:`Accept`
                                header of request
       :status 302: and then redirects to :http:get:`/posts/(int:post_id)`
       :status 400: when form parameters are missing


.. _roles:

Roles
-----

.. rst:role:: http:options

   Refers to the :rst:dir:`http:options` directive.

.. rst:role:: http:head

   Refers to the :rst:dir:`http:head` directive.

.. rst:role:: http:post

   Refers to the :rst:dir:`http:post` directive.

.. rst:role:: http:get

   Refers to the :rst:dir:`http:get` directive.

.. rst:role:: http:put

   Refers to the :rst:dir:`http:put` directive.

.. rst:role:: http:patch

   Refers to the :rst:dir:`http:patch` directive.

.. rst:role:: http:delete

   Refers to the :rst:dir:`http:delete` directive.

.. rst:role:: http:trace

   Refers to the :rst:dir:`http:trace` directive.

.. rst:role:: http:copy

   Refers to the :rst:dir:`http:copy` directive.

.. rst:role:: http:any

   Refers to the :rst:dir:`http:any` directive.

.. rst:role:: http:statuscode

   A reference to a HTTP status code. The text "`code` `Status Name`" is
   generated; in the HTML output, this text is a hyperlink to a web reference
   of the specified status code.

   For example:

   .. sourcecode:: rst

      - :http:statuscode:`404`
      - :http:statuscode:`200 Oll Korrect`

   will be rendered as:

       - :http:statuscode:`404`
       - :http:statuscode:`200 Oll Korrect`

   .. versionchanged:: 1.3.0
      It becomes to provide references to specification sections.

.. rst:role:: http:method

   A reference to a HTTP method (also known as *verb*). In the HTML output,
   this text is a hyperlink to a web reference of the specified HTTP method.

   For example:

   .. sourcecode:: rst

      It accepts :http:method:`post` only.

   It will render like this:

       It accepts :http:method:`post` only.

.. rst:role:: mimetype

   Exactly it doesn't belong to HTTP domain, but standard domain. It refers
   to the MIME type like :mimetype:`text/html`.

.. rst:role:: mailheader

   .. deprecated:: 1.3.0
      Use :rst:role:`http:header` instead.

.. rst:role:: http:header

   Similar to :rst:role:`mimetype` role, it doesn't belong to HTTP domain,
   but standard domain. It refers to the HTTP request/response header field
   like :http:header:`Content-Type`.

   Known HTTP headers:

   - :http:header:`Accept`
   - :http:header:`Accept-Charset`
   - :http:header:`Accept-Encoding`
   - :http:header:`Accept-Language`
   - :http:header:`Accept-Ranges`
   - :http:header:`Age`
   - :http:header:`Allow`
   - :http:header:`Authorization`
   - :http:header:`Cache-Control`
   - :http:header:`Connection`
   - :http:header:`Content-Encoding`
   - :http:header:`Content-Language`
   - :http:header:`Content-Length`
   - :http:header:`Content-Location`
   - :http:header:`Content-MD5`
   - :http:header:`Content-Range`
   - :http:header:`Content-Type`
   - :http:header:`Cookie`
   - :http:header:`Date`
   - :http:header:`Destination`
   - :http:header:`ETag`
   - :http:header:`Expect`
   - :http:header:`Expires`
   - :http:header:`From`
   - :http:header:`Host`
   - :http:header:`If-Match`
   - :http:header:`If-Modified-Since`
   - :http:header:`If-None-Match`
   - :http:header:`If-Range`
   - :http:header:`If-Unmodified-Since`
   - :http:header:`Last-Modified`
   - :http:header:`Last-Event-ID`
   - :http:header:`Link`
   - :http:header:`Location`
   - :http:header:`Max-Forwards`
   - :http:header:`Pragma`
   - :http:header:`Proxy-Authenticate`
   - :http:header:`Proxy-Authorization`
   - :http:header:`Range`
   - :http:header:`Referer`
   - :http:header:`Retry-After`
   - :http:header:`Server`
   - :http:header:`Set-Cookie`
   - :http:header:`TE`
   - :http:header:`Trailer`
   - :http:header:`Transfer-Encoding`
   - :http:header:`Upgrade`
   - :http:header:`User-Agent`
   - :http:header:`Vary`
   - :http:header:`Via`
   - :http:header:`WWW-Authenticate`
   - :http:header:`Warning`

   If HTTP header is unknown, the build error will be raised unless header has
   ``X-`` prefix which marks him as custom one like :http:header:`X-Foo-Bar`.

   .. versionadded:: 1.3.0


.. module:: sphinxcontrib.autohttp.flask

:mod:`sphinxcontrib.autohttp.flask` --- Exporting API reference from Flask app
------------------------------------------------------------------------------

.. versionadded:: 1.1

It generates RESTful HTTP API reference documentation from a Flask_
application's routing table, similar to :mod:`sphinx.ext.autodoc`.

In order to use it, add :mod:`sphinxcontrib.autohttp.flask` into
:data:`extensions` list of your Sphinx configuration (:file:`conf.py`) file::

    extensions = ['sphinxcontrib.autohttp.flask']

For example:

.. sourcecode:: rst

   .. autoflask:: autoflask_sampleapp:app
      :undoc-static:

will be rendered as:

    .. autoflask:: autoflask_sampleapp:app
       :undoc-static:

.. rst:directive:: .. autoflask:: module:app

   .. versionadded:: 1.1

   Generates HTTP API references from a Flask application. It takes an
   import name, like::

       your.webapplication.module:app

   Colon character (``:``) separates module path and application variable.
   Latter part can be more complex::

       your.webapplication.module:create_app(config='default.cfg')

   It's useful when a Flask application is created from the factory function
   (:func:`create_app`, in the above example).

   It takes several flag options as well.

   ``endpoints``
      Endpoints to generate a reference.

      .. sourcecode:: rst

         .. autoflask:: yourwebapp:app
            :endpoints: user, post, friends

      will document :func:`user`, :func:`post`, and :func:`friends`
      view functions, and

      .. sourcecode:: rst

         .. autoflask:: yourwebapp:app
            :endpoints:

      will document all endpoints in the flask app.

      For compatibility, omitting this option will produce the same effect
      like above.

      .. versionadded:: 1.1.8

   ``undoc-endpoints``
      Excludes specified endpoints from generated references.

      For example:

      .. sourcecode:: rst

         .. autoflask:: yourwebapp:app
            :undoc-endpoints: admin, admin_login

      will exclude :func:`admin`, :func:`admin_login` view functions.

      .. note::

         It is worth noting that the names of endpoints that are applied to
         blueprints are prefixed with the blueprint's name (e.g.
         blueprint.endpoint).

      .. note::

         While the `undoc-members`_ flag of :mod:`sphinx.ext.autodoc` extension
         includes members without docstrings, ``undoc-endpoints`` option has
         nothing to do with docstrings. It just excludes specified endpoints.

         .. _undoc-members: http://sphinx.pocoo.org/ext/autodoc.html#directive-automodule

   ``blueprints``
      Only include specified blueprints in generated references.

      .. versionadded:: 1.1.9

   ``undoc-blueprints``
      Excludes specified blueprints from generated references.

      .. versionadded:: 1.1.8

   ``undoc-static``
      Excludes a view function that serves static files, which is included
      in Flask by default.

   ``include-empty-docstring``
      View functions that don't have docstring (:attr:`__doc__`) are excluded
      by default. If this flag option has given, they become included also.

      .. versionadded:: 1.1.2

.. _Flask: http://flask.pocoo.org/



.. module:: sphinxcontrib.autohttp.bottle

:mod:`sphinxcontrib.autohttp.bottle` --- Exporting API reference from Bottle app
--------------------------------------------------------------------------------

It generates RESTful HTTP API reference documentation from a Bottle_
application's routing table, similar to :mod:`sphinx.ext.autodoc`.

In order to use it, add :mod:`sphinxcontrib.autohttp.bottle` into
:data:`extensions` list of your Sphinx configuration (:file:`conf.py`) file::

    extensions = ['sphinxcontrib.autohttp.bottle']

For example:

.. sourcecode:: rst

   .. autobottle:: autobottle_sampleapp:app

will be rendered as:

    .. autobottle:: autobottle_sampleapp:app

.. rst:directive:: .. autobottle:: module:app

   Generates HTTP API references from a Bottle application. It takes an
   import name, like::

       your.webapplication.module:app

   Colon character (``:``) separates module path and application variable.
   Latter part can be more complex::

       your.webapplication.module:create_app(config='default.cfg')

   It's useful when a Bottle application is created from the factory function
   (:func:`create_app`, in the above example).

   It takes several flag options as well.

   ``endpoints``
      Endpoints to generate a reference.

      .. sourcecode:: rst

         .. autobottle:: yourwebapp:app
            :endpoints: user, post, friends

      will document :func:`user`, :func:`post`, and :func:`friends`
      view functions, and

      .. sourcecode:: rst

         .. autobottle:: yourwebapp:app
            :endpoints:

      will document all endpoints in the bottle app.

      For compatibility, omitting this option will produce the same effect
      like above.

   ``undoc-endpoints``
      Excludes specified endpoints from generated references.

      For example:

      .. sourcecode:: rst

         .. autobottle:: yourwebapp:app
            :undoc-endpoints: admin, admin_login

      will exclude :func:`admin`, :func:`admin_login` view functions.

      .. note::

         While the `undoc-members`_ flag of :mod:`sphinx.ext.autodoc` extension
         includes members without docstrings, ``undoc-endpoints`` option has
         nothing to do with docstrings. It just excludes specified endpoints.

         .. _undoc-members: http://sphinx.pocoo.org/ext/autodoc.html#directive-automodule

   ``include-empty-docstring``
      View functions that don't have docstring (:attr:`__doc__`) are excluded
      by default. If this flag option has given, they become included also.

.. _Bottle: http://bottlepy.org/


.. module:: sphinxcontrib.autohttp.tornado

:mod:`sphinxcontrib.autohttp.tornado` --- Exporting API reference from Tornado app
----------------------------------------------------------------------------------

It generates RESTful HTTP API reference documentation from a Tornado_
application's routing table, similar to :mod:`sphinx.ext.autodoc`.

In order to use it, add :mod:`sphinxcontrib.autohttp.tornado` into
:data:`extensions` list of your Sphinx configuration (:file:`conf.py`) file::

    extensions = ['sphinxcontrib.autohttp.tornado']

For example:

.. sourcecode:: rst

   .. autotornado:: autotornado_sampleapp:app

will be rendered as:

    .. autotornado:: autotornado_sampleapp:app

.. rst:directive:: .. autotornado:: module:app

   Generates HTTP API references from a Tornado application. It takes an
   import name, like::

       your.webapplication.module:app

   Colon character (``:``) separates module path and application variable.

   It takes several flag options as well.

   ``endpoints``
      Endpoints to generate a reference.

      .. sourcecode:: rst

         .. autotornado:: yourwebapp:app
            :endpoints: User.get, User.post, Friends.get

      will document the :func:`get` and :func:`post` methods of the
      :class:`User` :class:`RequestHandler` and the :func:`get` method
      of the :class:`Friend` :class:`RequestHandler`, while

      .. sourcecode:: rst

         .. autotornado:: yourwebapp:app
            :endpoints:

      will document all endpoints in the tornado app.

      For compatibility, omitting this option will produce the same effect
      like above.

   ``undoc-endpoints``
      Excludes specified endpoints from generated references.

      For example:

      .. sourcecode:: rst

         .. autotornado:: yourwebapp:app
            :undoc-endpoints: admin, admin_login

      will exclude :func:`admin`, :func:`admin_login` view functions.

      .. note::

         While the `undoc-members`_ flag of :mod:`sphinx.ext.autodoc` extension
         includes members without docstrings, ``undoc-endpoints`` option has
         nothing to do with docstrings. It just excludes specified endpoints.

         .. _undoc-members: http://sphinx.pocoo.org/ext/autodoc.html#directive-automodule

   ``include-empty-docstring``
      View functions that don't have docstring (:attr:`__doc__`) are excluded
      by default. If this flag option has given, they become included also.

.. _Tornado: http://www.tornadoweb.org/


Author and License
------------------

The :mod:`sphinxcontrib.httpdomain` and :mod:`sphinxcontrib.autohttp`,
parts of :mod:`sphinxcontrib`, are written by `Hong Minhee`_
and distributed under BSD license.

The source code is mantained under `the common repository of contributed
extensions for Sphinx`__ (find the :file:`httpdomain` directory inside
the repository).

.. sourcecode:: console

   $ hg clone https://bitbucket.org/birkenfeld/sphinx-contrib
   $ cd sphinx-contrib/httpdomain

.. _Hong Minhee: http://dahlia.kr/
__ https://bitbucket.org/birkenfeld/sphinx-contrib


Changelog
---------

Version 1.4.0
`````````````

Released on August 13, 2015.

- Added :http:statuscode:`429 Too Many Requests` as a valid
  :rst:role:`http:statuscode`.  [:pull:`81` by DDBReloaded]
- Became to not resolve references if they can't be resolved.
  [:pull:`87` by Ken Robbins]
- Became to preserve endpoint ordering when ``:endpoints:`` option is given.
  [:pull:`88` by Dan Callaghan]
- Added status codes for WebDAV.  [:pull:`92` by Ewen Cheslack-Postava]
- Added CORS_ headers.  [:pull:`96` by Tomi Pieviläinen]
- Now :mod:`sphinxcontrib.autohttp.flask` supports multiple paths for
  endpoints using same HTTP method.  [:pull:`97` by Christian Felder]

.. _CORS: http://www.w3.org/TR/cors/


Version 1.3.0
`````````````

Released on July 31, 2014.

- ``jsonparameter``/``jsonparam``/``json`` became deprecated and split
  into ``reqjsonobj``/``reqjson``/``<jsonobj``/``<json`` and
  ``reqjsonarr``/``<jsonarr``.
  [:issue:`55`, :pull:`72` by Alexander Shorin]
- Support synopsis (short description in HTTP index),
  deprecation and noindex options for resources.
  [:issue:`55`, :pull:`72` by Alexander Shorin]
- Stabilize order of index items.
  [:issue:`55`, :pull:`72` by Alexander Shorin]
- Added :rst:directive:`http:any` directive and :rst:role:`http:any`
  role for ``ANY`` method.  [:issue:`55`, :pull:`72` by Alexander Shorin]
- Added :rst:directive:`http:copy` directive and :rst:role:`http:copy`
  role for ``COPY`` method.  [:issue:`55`, :pull:`72` by Alexander Shorin]
- Added :rst:role:`http:header` role that also creates reference to the
  related specification.  [:issue:`55`, :pull:`72` by Alexander Shorin]
- :rst:role:`http:statuscode` role became to provide references to
  specification sections.  [:issue:`55`, :pull:`72` by Alexander Shorin]
- Fixed Python 3 incompatibility of :mod:`autohttp.tornado`.
  [:pull:`61` by Dave Shawley]


Version 1.2.1
`````````````

Released on March 31, 2014.

- Fixed broken Python 2.6 compatibility.  [:pull:`41` by Kien Pham]
- Added missing link to six_ dependency.

.. _six: http://pythonhosted.org/six/


Version 1.2.0
`````````````

Released on October 19, 2013.

- Python 3 support!  [:pull:`34` by murchik, :pull:`39` Donald Stufft]
- Added support for Tornado webapps. (:mod:`sphinxcontrib.autohttp.tornado`)
  [:pull:`38` by Rodrigo Machado]


Version 1.1.9
`````````````

Released on August 8, 2013.

- Now Bottle_ apps can be loaded by :mod:`~sphinxcontrib.autohttp`.
  See :mod:`sphinxcontrib.autohttp.bottle` module.
  [patch_ by Jameel Al-Aziz]
- Added ``:reqheader:`` and ``:resheader:`` option flags.
- ``:jsonparameter:`` can be typed.  [:pull:`31` by Chuck Harmston]
- ``:queryparameter:`` can be typed.  [:pull:`37` by Viktor Haag]
- :rst:dir:`autoflask` and :rst:dir:`autobottle` directives now allow
  empty ``:endpoints:``, ``:undoc-endpoints:``, and ``:blueprints:``
  arguments.  [:pull:`33` by Michael Twomey]

.. _patch: https://github.com/jalaziz/sphinxcontrib-httpdomain


Version 1.1.8
`````````````

Released on April 10, 2013.

- Added better support for docstrings in :class:`flask.views.MethodView`.
  [:pull:`26` by Simon Metson]
- Added ``:jsonparameter:`` along side ``:form:`` and ``:query:`` flag options.
  [:pull:`25` by Adam Lowry]
- Fixed issue with undefined ``Value`` and ``umethod`` variables.
  [:pull:`23` by Sebastian Kalinowski and :pull:`24` by Viktor Haag]
- Now ``http`` Pygments lexer can Handle continuous header lines well.
- Added ``:undoc-blueprints:`` flag option to :rst:dir:`autoflask` directive.
  [:pull:`21` by Roman Podolyaka]
- Fixed :issue:`29`, a bug that :rst:dir:`autoflask` directive raised
  :exc:`UnicodeDecodeError` when it contains non-ASCII characters.
  [:issue:`29` and :pull:`18` by Eunchong Yu]
- Added ``:endpoints:`` flag option to :rst:dir:`autoflask` directive.
  [:pull:`17` by Eunchong Yu]

Version 1.1.7
`````````````

Released on March 28, 2012.

- Added :http:method:`PATCH` method support.  See :rst:role:`http:patch` role
  and :rst:dir:`http:patch` directive.
  [:pull:`9` and :pull:`10` by Jeffrey Finkelstein]
- The HTTP routing table can be grouped based on prefix by specifying
  :data:`http_index_ignore_prefixes` config in list of common prefixes to
  ignore.  [:pull:`7` and :pull:`8` by Andrey Popp]
- The order of HTTP routing table now provides sorting by path as key.
  Previously it was sorted by HTTP method and then by path, which is
  non-intuitive.  [:pull:`7` and :pull:`8` by Andrey Popp]


Version 1.1.6
`````````````

Released on December 16, 2011.

- Added ``http`` custom lexer for Pygments so that HTTP sessions can be
  highlighted in :rst:dir:`code-block` or :rst:dir:`sourcecode` directives.

Version 1.1.5
`````````````

Released on July 6, 2011.

- Flask 0.6--0.7 compatibility.  Flask renamed
  :attr:`~flask.Flask.static_path` attribute to
  :attr:`~flask.Flask.static_url_path`, so :rst:dir:`autoflask` also reflect
  the change.
  [:pull:`1` by Jeffrey Finkelstein]


Version 1.1.4
`````````````

Released on June 8, 2011.

- CPython compatibility
- PyPy compatibility


Version 1.1.3
`````````````

Released on June 8, 2011.

- PyPy compatibility


Version 1.1.2
`````````````

Released on June 4, 2011.

- Added ``:include-empty-docstring:`` flag option.


Version 1.1.1
`````````````

Released on June 4, 2011.

- Fixed a backward incompatibility bug.


Version 1.1
```````````

Released on June 4, 2011.

- Added :rst:dir:`autoflask` directive.


Version 1.0
```````````

Released on June 2, 2011.  The first release.
