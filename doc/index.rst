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

In order to use it, add :mod:`sphinxcontrib.httpdomain` into
:data:`extensions` list of your Sphinx configuration file (:file:`conf.py`)::

    extensions = ['sphinxcontrib.httpdomain']


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

``formparameter``, ``formparam``, ``fparam``, ``form``
   Description of parameter passed by request content body, encoded in
   :mimetype:`application/x-www-form-urlencoded` or
   :mimetype:`multipart/form-data`.

``jsonparameter``, ``jsonparam``, ``json``
   Description of a parameter passed by request content body, encoded in
   :mimetype:`application/json`.

   .. versionadded:: 1.1.8

   .. versionchanged:: 1.1.9

      It can be typed e.g.:

      .. sourcecode:: rst

         :jsonparam string title: the post title
         :jsonparam string body: the post body
         :jsonparam boolean sticky: whether it's sticky or not

``requestheader``, ``reqheader``
   Description of request header field.

   .. versionadded:: 1.1.9

``responseheader``, ``resheader``
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

   Similar to :rst:role:`mimetype` role, it doesn't belong to HTTP domain,
   but standard domain. It refers to the HTTP request/response header field
   like :mailheader:`Content-Type`.


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

      will document all endpoints in the flask app.

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

Version 1.1.9
`````````````
To be released.

- Now Bottle_ apps can be loaded by :mod:`~sphinxcontrib.autohttp`.
  See :mod:`sphinxcontrib.autohttp.bottle` module.
  [patch_ by Jameel Al-Aziz]
- Added ``:reqheader:`` and ``:resheader:`` option flags.
- ``:jsonparameter:`` can be typed.  [:pull:`31` by Chuck Harmston]

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
