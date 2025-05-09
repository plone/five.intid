Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.0.1 (2025-03-07)
------------------

Bug fixes:


- Replace `pkg_resources` with `importlib.metadata` @gforcada (#4126)


3.0.0 (2025-02-18)
------------------

Breaking changes:


- Drop support for ``pkg_resources`` namespace and replace it with PEP 420 native namespace. (pep-420)


2.0.0 (2023-10-07)
------------------

Breaking changes:


- Drop support for python 2.7.
  [gforcada] (#1)


Internal:


- Update configuration files.
  [plone devs] (cfffba8c)


1.2.7 (2023-02-22)
------------------

Bug fixes:


- Add configuration with plone/meta.
  [gforcada] (#1)


1.2.6 (2020-05-06)
------------------

Bug fixes:


- Fix deprecation warnings.
  Update ``setup.py`` to depend on ``Zope2`` or ``Zope``, depending on Python version.
  [jensens] (#1)
- Fix test to work correctly with ``zope.interface >= 5.1``.
  [jensens] (#17)


1.2.5 (2020-03-13)
------------------

Bug fixes:


- Fixed ModuleNotFoundError: No module named 'App.class_init' on Zope 5.
  [maurits] (#15)


1.2.4 (2019-10-12)
------------------

Bug fixes:


- Also catch KeyError when traversing to fix creating relations during Copy&Paste in Zope 4.
  Fixes https://github.com/plone/Products.CMFPlone/issues/2866
  [pbauer] (#12)
- When looking up back-references the lookup using unrestrictedTraverse was way to slow.
  A simplified traverse speeds up the lookup by up 80x. [jensens, 2silver] (#14)


1.2.3 (2019-06-19)
------------------

Bug fixes:


- Properly update the persistent objects stored in the initid utility btrees [ale-rt] (#8)
- Also catch KeyError when traversing to fix creating relations during Copy&Paste in Zope 4.
  Fixes https://github.com/plone/Products.CMFPlone/issues/2866
  [pbauer] (#12)


1.2.2 (2019-05-01)
------------------

Bug fixes:


- Fix oid and root_oid that might have been accidentally converted to text when a DB was migrated from py2.
  [pbauer] (#7)


1.2.1 (2019-02-13)
------------------

Bug fixes:


- Avoid a deprecation warning. [gforcada] (#6)


1.2.0 (2018-11-07)
------------------

Bug fixes:

- Fix doctests in Python 3.
  [ale-rt]
- Adapt raised errors to changes in zope.intid.
  (This makes the tests incompatible with Zope 2.13.)
  [pbauer]


1.1.2 (2016-09-09)
------------------

Bug fixes:

- Prevent errors on ``removeIntIdSubscriber`` when the ``IKeyReference`` adapter
  raises a ``NotYet``, e.g. because the object does not have a proper path.
  [ale-rt]


1.1.1 (2016-08-19)
------------------

Fixes:

- Acquisition-unwrap each item in the aq_iter chain, as ``getSite().__parent__`` might return an object acquired from the original context which breaks the parent loop detection.
  [thet]

- Prevent errors on ``moveIntIdSubscriber`` when the ``IKeyReference`` adapter
  raises a ``NotYet``, e.g. because the object does not have a proper path.
  [ale-rt]


1.1.0 (2016-02-14)
------------------

New:

- Enhancement: follow PEP8 and Plone code conventions
  [jensens]

Fixes:

- Fix: Make it work with Acquisition>=4.0.1 (and require the version).
  Circular acquisitions were - prior to the above version - not
  detected.  Now they are and adaption just fails with a "Could not
  adapt" for circulars.  Any attribute access fails with a verbose
  RuntimeError.  Cleanup also circular containment workarounds.
  [jensens]

1.0.3 - 2012-10-05
------------------

- Make sure the IConnection adapter works for unwrapped persistent
  objects.
  [davisagli]

1.0.2 - 2011-12-02
------------------

- Only ignore 'temporary' objects in the ObjectAddedEvent event handler.
  [mj]

1.0.1 - 2011-11-30
------------------

- Ignore 'temporary' objects (in the Plone portal_factory tool).
  [mj]

1.0 - 2011-10-10
----------------

- Remove last `zope.app` dependency.
  [hannosch]

- Remove intid browser views.
  [hannosch]

- Modernize code, adept to Zope 2.13.
  [hannosch]

0.5.2 - January 22, 2011
------------------------

- Import getAllUtilitiesRegisteredFor directly from zope.component and
  remove dependency on zope.app.zapi.
  [Arfrever]

- Fix chameleon template error.
  [robgietema]

0.5.1 - August 4, 2010
----------------------

- Fix tests to pass with the corrected tp_name of ImplicitAcquisitionWrapper
  in Acquisition 2.13.1.
  [davisagli]

0.5.0 - February 6, 2010
------------------------

- Use only non-deprecated zope imports, five.intid now only supports
  Zope 2.12+.
  [alecm]

0.4.4 - February 6, 2010
------------------------

- Fix POSKeyError when the root object is not in the same database
  than the object you are trying to resolve to.
  [thefunny42]

- Fixed all deprecated imports and updated setup.py
  [thet, wichert]

- Fixed tests to reflect changed Zope API
  [thet]

0.4.3 - July 19, 2009
---------------------

- When looking for an object by path, treat an AttributeError the same as a
  NotFound error. unrestrictedTraverse() raises an AttributeError in certain
  cases when it can't traverse.
  [optilude]

0.4.2 - Apr 26, 2009
--------------------

- Install utility in a more permanent manner.
  [alecm]

- Drop `five:traversable` statement. It was deprecated since Zope 2.10.
  [hannosch]

- Use `objectEventNotify` from zope.component.event instead of zope.app.event.
  The later was deprecated since Zope 2.10.
  [hannosch]

- Specify package dependencies.
  [hannosch]

0.4.1 - Mar 17, 2009
--------------------

- Fix missing zcml file in prior release

0.4.0 - Mar 17, 2009
--------------------

- Raise NotYet exception in the default keyreference constructor when the
  object does not yet have a proper path. This avoids problems of premature
  key references being created and pointing to the parent of the object or
  a non-existent object.
  [optilude]

0.3.0 - Nov 07, 2008
--------------------

- Add unreferenceable implementations of intid event handlers and IKeyReference
  to deal with IPersistent objects that are never actually persisted, such as
  the CMFCore directory view objects.
  [mj]

- Remove the explicit exceptions for CMFCore directory view objects and use
  subscriber and adapter registrations against unreferenceable instead.
  [mj]

0.2.1 - Nov 05, 2008
--------------------

- Avoid unnecessary adapter lookups in __cmp__ as __cmp__
  is called rather often and is performance sensitive.
  Cumulative time now 0.080 vs previous 1.820 for 6000 compares
  when profiling.
  [tesdal]

- Avoid redundant __cmp__ calls in BTree traversal.
  [tesdal]

0.2.0 - May 20, 2008
--------------------

- Cleanup documentation a little bit so it can be used for the pypi page.
  [wichert]

- Many changes by many people.
  [alecm, hannosch, maurits, mborch, reinout, rockt, witsch]


0.1.4 - November 11, 2006
-------------------------

- First public release.
  [brcwhit]
