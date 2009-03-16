import doctest
from zope.app.testing import placelesssetup
from persistent import Persistent
from zope.app.component.hooks import setHooks, setSite

from Products.Five.tests.testing.simplecontent import (
    SimpleContent,
    ISimpleContent,
    manage_addSimpleContent,
    )
from Products.Five import zcml
from five.intid.lsm import USE_LSM
from five.intid import site


optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

class DemoPersistent(Persistent):
    """ Demo persistent object """
    test = 'test object'
    __name__ = 'Test Object'

NOTIFIED=[None]

def setNotified(event):
    NOTIFIED[0] = "%s %s" %(event.object, event)


def setUp(app):
    # enable zcml and site hooks
    placelesssetup.setUp()
    import Products.Five
    from five import intid
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('test.zcml', intid)
    if not USE_LSM:
        # monkey in our hooks
        from Products.Five.site.metaconfigure import classSiteHook
        from Products.Five.site.localsite import FiveSite
        from zope.interface import classImplements
        from zope.app.component.interfaces import IPossibleSite
        klass = app.__class__
        classSiteHook(klass, FiveSite)
        classImplements(klass, IPossibleSite)
    setHooks()

def tearDown():
    placelesssetup.tearDown()

def test_suite():
    import unittest
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    from zope.testing.doctest import DocTestSuite
    integration = FunctionalDocFileSuite(
        'README.txt',
        package='five.intid',
        optionflags=optionflags
        )
    return unittest.TestSuite((integration,))
