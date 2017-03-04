Changelog
---------

Version 1.6.0
`````````````

To be released.

- Added ``groupby`` option to :rst:`.. autoflask::` directive.  It makes
  paths be grouped by their view functions.  [:pull:`147` by Jiangge Zhang]
- Fixed a bug that :rst:dir:`autoflask` directive had excluded nonsignificant
  routes with :http:method:`HEAD`/:http:method:`OPTIONS`.  [:issue:`165`]


Version 1.5.0
`````````````

Released on May 30, 2016.

- Added :mod:`sphinxcontrib.autohttp.flaskqref` for generating quick reference
  table.  [:pull:`80`, :pull:`100` by Harry Raaymakers]
- :rst:dir:`autoflask` now supports ``:modules:`` and ``:undoc-modules:``
  arguments, used to filter documented flask endpoints by view module
  [:pull:`102` by Ivelin Slavov]
- Added ``:order:`` option to :rst:dir:`autoflask` directive.
  [:pull:`103` by Justin Gruca]
- HTTP message headers become to link the recent RFCs (:rfc:`7230`, :rfc:`7231`,
  :rfc:`7232`, :rfc:`7233`, :rfc:`7234`, :rfc:`7235`, :rfc:`7236`, :rfc:`7237`,
  that are separated to multiple RFCs from the old one) instead of :rfc:`2615`
  which is replaced by them in 2014.
  [:pull:`105`, :pull:`106` by Alex C. (iscandr)]
- Support ``resolve_any_xref`` method introduced since Sphinx 1.3
  [:pull:`108` by Takayuki Shimizukawa]
- It no more warns non-standard message headers without ``X-`` prefix
  according as the deprecation of the practice of prefixing the names of
  unstandardized parameters with ``X-`` in all IETF protocols since June 2012
  by :rfc:`6648`.  [:pull:`114` by Dolan Murvihill]
- Fixed performance bottleneck in doctree lookup by adding a cache for it.
  [:pull:`115` by Kai Lautaportti]
- Added :http:statuscode:`451` to :rst:role:`http:statuscode`.
  [:pull:`117` by Xavier Oliver]


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
- Added :rst:dir:`http:any` directive and :rst:role:`http:any`
  role for ``ANY`` method.  [:issue:`55`, :pull:`72` by Alexander Shorin]
- Added :rst:dir:`http:copy` directive and :rst:role:`http:copy`
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
