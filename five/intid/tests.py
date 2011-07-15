import doctest

from persistent import Persistent
from zope.app.testing import placelesssetup
from zope.site.hooks import setHooks
from Zope2.App import zcml

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
NOTIFIED = [None]


class DemoPersistent(Persistent):
    """ Demo persistent object """
    test = 'test object'
    __name__ = 'Test Object'


def setNotified(event):
    NOTIFIED[0] = "%s %s" % (event.object, event)


def setUp(app):
    # enable zcml and site hooks
    placelesssetup.setUp()
    import Products.Five
    from five import intid
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('test.zcml', intid)
    setHooks()

def tearDown():
    placelesssetup.tearDown()


def test_suite():
    import unittest
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    return unittest.TestSuite([
        FunctionalDocFileSuite(
            'README.txt',
            package='five.intid',
            optionflags=optionflags,
        )
    ])
