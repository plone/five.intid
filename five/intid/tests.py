import doctest

from lsm import USE_LSM

from collective.testing.layer import ZCMLLayer
from persistent import Persistent


optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS
from Products.Five.tests.testing.simplecontent import SimpleContent, ISimpleContent, manage_addSimpleContent
from five.intid import site

from Products.Five import zcml
from zope.app.component.hooks import setSite, getSite, setHooks
from cStringIO import StringIO

class DemoPersistent(Persistent):
    """ Demo persistent object """
    test = 'test object'
    __name__ = 'Test Object'

class zope(object):
    import zope.interface as interface
    import zope.component as component

NOTIFIED=[None]

def setNotified(event):
    NOTIFIED[0] = "%s %s" %(event.object, event)

from five import intid
class FiveIntIdEventLayer(ZCMLLayer):
    import Zope2
    @classmethod
    def setUp(cls):
        if not USE_LSM:
            # monkeypatch app as site
            from collective.testing.utils import monkeyAppAsSite
            monkeyAppAsSite()
        zcml.load_config('test.zcml', intid)
        setHooks()

def test_suite():
    import unittest
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    from zope.testing.doctest import DocTestSuite
    integration = FunctionalDocFileSuite(
        'README.txt',
        package='five.intid',
        optionflags=optionflags
        )
    integration.layer = FiveIntIdEventLayer
    utils = DocTestSuite("five.intid.utils")
    return unittest.TestSuite((integration, utils))
