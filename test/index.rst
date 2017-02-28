.. module:: sphinxcontrib.httpdomain

:mod:`sphinxcontrib.httpdomain` --- Documenting RESTful HTTP APIs
=================================================================

Directives
~~~~~~~~~~

.. http:patch:: /users/(int:user_id)/posts/(tag)
.. http:options:: /users/(int:user_id)/posts/(tag)
.. http:get:: /users/(int:user_id)/posts/(tag)
.. http:head:: /users/(int:user_id)/posts/(tag)
.. http:post:: /users/(int:user_id)/posts/(tag)
.. http:put:: /users/(int:user_id)/posts/(tag)
.. http:delete:: /users/(int:user_id)/posts/(tag)
.. http:trace:: /users/(int:user_id)/posts/(tag)
.. http:connect:: /users/(int:user_id)/posts/(tag)
.. http:copy:: /users/(int:user_id)/posts/(tag)

Sourcecode
~~~~~~~~~~

.. sourcecode:: http

   GET /users/123/posts/web HTTP/1.1
   Host: example.com
   Accept: application/json, text/javascript

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

Resource fields
~~~~~~~~~~~~~~~

.. http:get:: /foo

   :query resource: description for ``resource``
   :statuscode 200: description for 200
   :statuscode 404: description for 404

.. http:get:: /short-syntax

   :<header Accept: :mimetype:`application/json`
   :<json string foo: Foo key value
   :<json number bar: Bar key value
   :>header Content-Type: :mimetype:`application/json`
   :>jsonarr string baz: Some baz field
   :code 200: Success


Options
~~~~~~~

.. http:get:: /bar
   :noindex:

.. http:put:: /baz
   :synopsis: Something special

.. http:post:: /baz
   :deprecated:
   :synopsis: Something special, but use PUT instead

Roles
~~~~~

Referring to existing directives
................................

:http:patch:`/users/(int:user_id)/posts/(tag)`

:http:options:`/users/(int:user_id)/posts/(tag)`

:http:get:`/users/(int:user_id)/posts/(tag)`

:http:head:`/users/(int:user_id)/posts/(tag)`

:http:post:`/users/(int:user_id)/posts/(tag)`

:http:put:`/users/(int:user_id)/posts/(tag)`

:http:delete:`/users/(int:user_id)/posts/(tag)`

:http:trace:`/users/(int:user_id)/posts/(tag)`

:http:connect:`/users/(int:user_id)/posts/(tag)`

Method roles
............

:http:method:`patch`

:http:method:`options`

:http:method:`get`

:http:method:`head`

:http:method:`post`

:http:method:`put`

:http:method:`delete`

:http:method:`trace`

:http:method:`connect`

Here be Errors!
~~~~~~~~~~~~~~~

A request with method :http:method:`foo` followed by :http:header:`bar` and
:http:header:`x-baz` headers receives response with :http:statuscode:`42 Answer`
status code.

.. module:: sphinxcontrib.autohttp.flask

:mod:`sphinxcontrib.autohttp.flask` --- Exporting API reference from Flask app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic option
............

.. autoflask:: autoflask_sampleapp:app
   :undoc-static:

Basic option with empty args
............................

.. autoflask:: autoflask_sampleapp:app
   :undoc-static:
   :endpoints:
   :undoc-endpoints:
   :undoc-blueprints:

Basic option with ordering by path
..................................

.. autoflask:: autoflask_sampleapp:app
   :undoc-static:
   :endpoints:
   :undoc-endpoints:
   :undoc-blueprints:
   :order: path

Filter some endpoints
......................

.. autoflask:: autoflask_sampleapp:app
   :endpoints: user, post
   :undoc-static:

Method View
...........

.. autoflask:: autoflask_methodview:app
   :undoc-static:

Grouped Method View
....................

.. autoflask:: autoflask_methodview:app
   :groupby: view
   :undoc-static:

Documenting by non-ASCII characters
...................................

.. autoflask:: autoflask_alternative_lang:app
   :undoc-static:
