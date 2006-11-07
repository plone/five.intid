import doctest
# monkeypatch app as site
from collective.testing.utils import monkeyAppAsSite
monkeyAppAsSite()

from collective.testing.layer import ZCMLLayer
from collective.testing.subscribers import setBuffer, setFilter

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS
from Products.Five.tests.testing.simplecontent import SimpleContent, ISimpleContent, manage_addSimpleContent
from five.intid import site

from Products.Five import zcml
from zope.app.component.hooks import setSite, getSite, setHooks
from cStringIO import StringIO

class zope(object):
    import zope.interface as interface
    import zope.component as component

# create test namespace
test_ns = dict(manage_addSimpleContent=manage_addSimpleContent,
               SimpleContent=SimpleContent,
               site=site,
               setEventBuffer=setBuffer,
               StringIO=StringIO,
               getSite=getSite,
               setSite=setSite,
               zope = zope
               )

from zope.app.intid.interfaces import IIntIdRemovedEvent
from zope.app.intid.interfaces import IIntIdAddedEvent

setFilter()

NOTIFIED=[None]

def setNotified(obj, event):
    NOTIFIED[0] = "%s %s" %(obj, event)

from five import intid
class FiveIntIdEventLayer(ZCMLLayer):
    import Zope2
    @classmethod
    def setUp(cls):
        zcml.load_config('test.zcml', intid)
        setHooks()

def test_suite():
    import unittest
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    from zope.testing.doctest import DocTestSuite
    integration = FunctionalDocFileSuite(
        'README.txt',
        optionflags=optionflags,
        package='five.intid',
        globs=test_ns,
        )
    integration.layer = FiveIntIdEventLayer
    utils = DocTestSuite("five.intid.utils")
    return unittest.TestSuite((integration, utils))
