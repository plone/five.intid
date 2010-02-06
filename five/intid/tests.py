import doctest

from zope.app.testing import placelesssetup
from persistent import Persistent
from zope.site.hooks import setHooks, setSite

from Products.Five.tests.testing.simplecontent import (
    SimpleContent,
    ISimpleContent,
    manage_addSimpleContent,
    )
from Products.Five import zcml
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
    setHooks()

def tearDown():
    placelesssetup.tearDown()


TESTFILES = [
    'README.txt',
    #'tracking.txt',
]

def test_suite():
    import unittest
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    from zope.testing.doctest import DocTestSuite
    return unittest.TestSuite([
        FunctionalDocFileSuite(
            file,
            package='five.intid',
            optionflags=optionflags,
        ) for file in TESTFILES
    ])

#
