:orphan:

Changelog
---------

Version 2.0.0
`````````````

unreleased

- Add support for Python 3.7 up to 3.12.
- Drop support for Python 3.6 and older.

Version 1.8.0
`````````````

Released on September 23, 2020

- Make the generated routing table referencable using the 'routingtable'
  label. [:pull:`19` by David Douard]
- Add support for parallel sphinx builds. Increases sphinx version requirement to 1.6
  [:pull:`31` by Daniel Hofmann]
- Remove references to the generic ``:py:obj:`` role [:pull:`54` by Stephen Finucane]
- Remove imports and calls to deprecated function force_decode who was removed
  starting with sphinx 4.0 [:pull:`49` by Florian Masy]
- Be explicit about what versions of Python are supports (2.7, and 3.5+). This will
  be the last version to support Python 2.7 and 3.5, version 2.0 will require 3.6+.


Version 1.7.0
`````````````

Released on July 1, 2018.

- Implemented ``:autoquickref:`` option that use available information to
  build a ``quickref``. [:pull:`9` by Alexandre Bonnetain]
- Improved :mod:`sphinxcontrib.autohttp.tornado` compatibility with Tornado
  4.5 and newer. `Tornado 4.5 <http://www.tornadoweb.org/en/stable/releases/v4.5.0.html>`_
  introduced the ``Rule`` class and made ``URLSpec`` a subclass of it, so certain
  rule attributes required updating. [:issue:`7`, :pull:`11` by Robert Zeigler]


Version 1.6.1
`````````````

Released on March 3, 2018.

- Remove references to the ``sphinx.util.compat`` module which was deprecated
  in Sphinx 1.6 and removed in 1.7.  [:issue:`5`, :pull:`4` by Jeremy Cline]
- Made :mod:`sphinxcontrib.autohttp.tornado` compatible with Tornado 4.5 and
  newer.  `Tornado 4.5 <http://www.tornadoweb.org/en/stable/releases/v4.5.0.html>`_
  removed the ``handlers`` attribute from ``tornado.web.Application``.
  [:pull:`3` by Dave Shawley]


Version 1.6.0
`````````````

Released on January 13, 2018.

- Minimum compatible version of Sphinx became changed to 1.5.
- Fixed a bug that prevented building :mod:`sphinxcontrib.autohttp`
  from building properly with Sphinx 1.6 or higher.
  [:oldissue:`182`, :oldpull:`152` by Dave Shawley]
- Use HTTPS for ``:rfc:`` generated links. [:oldpull:`144` by Devin Sevilla]
- Added ``groupby`` option to :rst:dir:`autoflask` directive.  It makes
  paths be grouped by their view functions.  [:oldpull:`147` by Jiangge Zhang]
- Fixed a bug that :rst:dir:`autoflask` directive had excluded nonsignificant
  routes with :http:method:`HEAD`/:http:method:`OPTIONS`.  [:oldissue:`165`]


Version 1.5.0
`````````````

Released on May 30, 2016.

- Added :mod:`sphinxcontrib.autohttp.flaskqref` for generating quick reference
  table.  [:oldpull:`80`, :oldpull:`100` by Harry Raaymakers]
- :rst:dir:`autoflask` now supports ``:modules:`` and ``:undoc-modules:``
  arguments, used to filter documented flask endpoints by view module
  [:oldpull:`102` by Ivelin Slavov]
- Added ``:order:`` option to :rst:dir:`autoflask` directive.
  [:oldpull:`103` by Justin Gruca]
- HTTP message headers become to link the recent RFCs (:rfc:`7230`, :rfc:`7231`,
  :rfc:`7232`, :rfc:`7233`, :rfc:`7234`, :rfc:`7235`, :rfc:`7236`, :rfc:`7237`,
  that are separated to multiple RFCs from the old one) instead of :rfc:`2615`
  which is replaced by them in 2014.
  [:oldpull:`105`, :oldpull:`106` by Alex C. (iscandr)]
- Support ``resolve_any_xref`` method introduced since Sphinx 1.3
  [:oldpull:`108` by Takayuki Shimizukawa]
- It no more warns non-standard message headers without ``X-`` prefix
  according as the deprecation of the practice of prefixing the names of
  unstandardized parameters with ``X-`` in all IETF protocols since June 2012
  by :rfc:`6648`.  [:oldpull:`114` by Dolan Murvihill]
- Fixed performance bottleneck in doctree lookup by adding a cache for it.
  [:oldpull:`115` by Kai Lautaportti]
- Added :http:statuscode:`451` to :rst:role:`http:statuscode`.
  [:oldpull:`117` by Xavier Oliver]


Version 1.4.0
`````````````

Released on August 13, 2015.

- Added :http:statuscode:`429 Too Many Requests` as a valid
  :rst:role:`http:statuscode`.  [:oldpull:`81` by DDBReloaded]
- Became to not resolve references if they can't be resolved.
  [:oldpull:`87` by Ken Robbins]
- Became to preserve endpoint ordering when ``:endpoints:`` option is given.
  [:oldpull:`88` by Dan Callaghan]
- Added status codes for WebDAV.  [:oldpull:`92` by Ewen Cheslack-Postava]
- Added CORS_ headers.  [:oldpull:`96` by Tomi Pieviläinen]
- Now :mod:`sphinxcontrib.autohttp.flask` supports multiple paths for
  endpoints using same HTTP method.  [:oldpull:`97` by Christian Felder]

.. _CORS: http://www.w3.org/TR/cors/


Version 1.3.0
`````````````

Released on July 31, 2014.

- ``jsonparameter``/``jsonparam``/``json`` became deprecated and split
  into ``reqjsonobj``/``reqjson``/``<jsonobj``/``<json`` and
  ``reqjsonarr``/``<jsonarr``.
  [:oldissue:`55`, :oldpull:`72` by Alexander Shorin]
- Support synopsis (short description in HTTP index),
  deprecation and noindex options for resources.
  [:oldissue:`55`, :oldpull:`72` by Alexander Shorin]
- Stabilize order of index items.
  [:oldissue:`55`, :oldpull:`72` by Alexander Shorin]
- Added :rst:dir:`http:any` directive and :rst:role:`http:any`
  role for ``ANY`` method.  [:oldissue:`55`, :oldpull:`72` by Alexander Shorin]
- Added :rst:dir:`http:copy` directive and :rst:role:`http:copy`
  role for ``COPY`` method.  [:oldissue:`55`, :oldpull:`72` by Alexander Shorin]
- Added :rst:role:`http:header` role that also creates reference to the
  related specification.  [:oldissue:`55`, :oldpull:`72` by Alexander Shorin]
- :rst:role:`http:statuscode` role became to provide references to
  specification sections.  [:oldissue:`55`, :oldpull:`72` by Alexander Shorin]
- Fixed Python 3 incompatibility of :mod:`autohttp.tornado`.
  [:oldpull:`61` by Dave Shawley]


Version 1.2.1
`````````````

Released on March 31, 2014.

- Fixed broken Python 2.6 compatibility.  [:oldpull:`41` by Kien Pham]
- Added missing link to six_ dependency.

.. _six: https://six.readthedocs.io//


Version 1.2.0
`````````````

Released on October 19, 2013.

- Python 3 support!  [:oldpull:`34` by murchik, :oldpull:`39` Donald Stufft]
- Added support for Tornado webapps. (:mod:`sphinxcontrib.autohttp.tornado`)
  [:oldpull:`38` by Rodrigo Machado]


Version 1.1.9
`````````````

Released on August 8, 2013.

- Now Bottle_ apps can be loaded by :mod:`~sphinxcontrib.autohttp`.
  See :mod:`sphinxcontrib.autohttp.bottle` module.
  [patch_ by Jameel Al-Aziz]
- Added ``:reqheader:`` and ``:resheader:`` option flags.
- ``:jsonparameter:`` can be typed.  [:oldpull:`31` by Chuck Harmston]
- ``:queryparameter:`` can be typed.  [:oldpull:`37` by Viktor Haag]
- :rst:dir:`autoflask` and :rst:dir:`autobottle` directives now allow
  empty ``:endpoints:``, ``:undoc-endpoints:``, and ``:blueprints:``
  arguments.  [:oldpull:`33` by Michael Twomey]

.. _patch: https://github.com/jalaziz/sphinxcontrib-httpdomain
.. _Bottle: http://bottlepy.org/


Version 1.1.8
`````````````

Released on April 10, 2013.

- Added better support for docstrings in :class:`flask.views.MethodView`.
  [:oldpull:`26` by Simon Metson]
- Added ``:jsonparameter:`` along side ``:form:`` and ``:query:`` flag options.
  [:oldpull:`25` by Adam Lowry]
- Fixed issue with undefined ``Value`` and ``umethod`` variables.
  [:oldpull:`23` by Sebastian Kalinowski and :oldpull:`24` by Viktor Haag]
- Now ``http`` Pygments lexer can Handle continuous header lines well.
- Added ``:undoc-blueprints:`` flag option to :rst:dir:`autoflask` directive.
  [:oldpull:`21` by Roman Podolyaka]
- Fixed :oldissue:`29`, a bug that :rst:dir:`autoflask` directive raised
  :exc:`UnicodeDecodeError` when it contains non-ASCII characters.
  [:oldissue:`29` and :oldpull:`18` by Eunchong Yu]
- Added ``:endpoints:`` flag option to :rst:dir:`autoflask` directive.
  [:oldpull:`17` by Eunchong Yu]

Version 1.1.7
`````````````

Released on March 28, 2012.

- Added :http:method:`PATCH` method support.  See :rst:role:`http:patch` role
  and :rst:dir:`http:patch` directive.
  [:oldpull:`9` and :oldpull:`10` by Jeffrey Finkelstein]
- The HTTP routing table can be grouped based on prefix by specifying
  :data:`http_index_ignore_prefixes` config in list of common prefixes to
  ignore.  [:oldpull:`7` and :oldpull:`8` by Andrey Popp]
- The order of HTTP routing table now provides sorting by path as key.
  Previously it was sorted by HTTP method and then by path, which is
  non-intuitive.  [:oldpull:`7` and :oldpull:`8` by Andrey Popp]


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
  [:oldpull:`1` by Jeffrey Finkelstein]


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
