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
   See the following :mod:`sphinxcontrib.autohttp` modules:

   Module :mod:`sphinxcontrib.autohttp.flask`
      Reflection for Flask_ webapps.

   Module :mod:`sphinxcontrib.autohttp.flaskqref` 
      Quick reference rendering with :mod:`sphinxcontrib.autohttp.flask`

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

   .. deprecated:: 1.5.0
        strict mode no longer warns on non-standard header prefixes.


``http_index_ignore_prefixes``
   Strips the leading segments from the endpoint paths by given list
   of prefixes::

       http_index_ignore_prefixes = ['/internal', '/_proxy']

   .. versionadded:: 1.3.0

``http_index_shortname``
   Short name of the index which will appear on every page::

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

   If the HTTP header is known, the text is a hyperlink to a web reference of
   the specified header.

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

   .. versionadded:: 1.3.0

   .. versionchanged:: 1.5.0

        No longer emits warnings for unrecognized headers

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

   ``modules``
      Only include specified view modules in generated references.

      For example:

      .. sourcecode:: rst

         .. autoflask:: yourwebapp:app
            :modules: yourwebapp.views.admin

      will include only views in ``yourwebapp.views.admin`` module

      .. versionadded:: 1.5.0

   ``undoc-modules``
      Excludes specified view modules from generated references.

      .. versionadded:: 1.5.0

   ``undoc-static``
      Excludes a view function that serves static files, which is included
      in Flask by default.

   ``order``
      Determines the order in which endpoints are listed. Currently only
      ``path`` is supported.

      For example:

      .. sourcecode:: rst

         .. autoflask:: yourwebapp:app
            :endpoints:
            :order: path

      will document all endpoints in the flask app, ordered by their route
      paths.

      .. versionadded:: 1.5.0

   ``groupby``
      Determines the strategy to group paths. Currently only ``view`` is
      supported. Specified this will group paths by their view functions.

      .. versionadded:: 1.6.0

   ``include-empty-docstring``
      View functions that don't have docstring (:attr:`__doc__`) are excluded
      by default. If this flag option has given, they become included also.

      .. versionadded:: 1.1.2

.. _Flask: http://flask.pocoo.org/


.. module:: sphinxcontrib.autohttp.flaskqref

:mod:`sphinxcontrib.autohttp.flaskqref` --- Quick API reference for Flask app
------------------------------------------------------------------------------

.. versionadded:: 1.5.0

This generates a quick API reference table for the route documentation
produced by :mod:`sphinxcontrib.autohttp.flask`

To use it, both :mod:`sphinxcontrib.autohttp.flask` and :mod:`sphinxcontrib.autohttp.flaskqref` need to be added into the extensions 
of your configuration (:file:`conf.py`) file::

    extensions = ['sphinxcontrib.autohttp.flask',
                  'sphinxcontrib.autohttp.flaskqref']

.. rst:directive:: .. qrefflask:: module:app

   .. versionadded:: 1.5.0

   Generates HTTP API references from a Flask application and places these
   in a list-table with quick reference links. The usage and options are identical
   to that of :mod:`sphinxcontrib.autohttp.flask`


Basic usage
```````````

You typically would place the quick reference table near the top of your docco
and use *.. autoflask::* further down.

Routes that are to be included in the quick reference table require 
the following rst comment to be added to their doc string:

.. sourcecode:: rst

    .. :quickref: [<resource>;] <short description>

<resource> is optional, if used a semi-colon separates it from <short description>
The table is grouped and sorted by <resource>.

``<resource>``
   This is the resource name of the operation.  The name maybe the same for a number
   of operations and enables grouping these together. 

``<short description>``
   A brief description what the operation does.

For example:

.. sourcecode:: python

    @app.route('/<user>')
    def user(user):
        """User profile page.

        .. :quickref: User; Get Profile Page
     
        my docco here   
        """
        return 'hi, ' + user


The quick reference table is defined as:

.. sourcecode:: rst

   .. qrefflask:: autoflask_sampleapp:app
      :undoc-static:

Using the autoflask_sampleapp with *.. :quickref:* annotations,
this is rendered as:

   .. qrefflask:: autoflask_sampleapp:app
      :undoc-static:


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

.. _Hong Minhee: https://hongminhee.org/
__ https://bitbucket.org/birkenfeld/sphinx-contrib


.. include:: changelog.rst
