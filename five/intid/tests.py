# -*- coding: utf-8 -*-
from persistent import Persistent
from Testing.ZopeTestCase import placeless
from Zope2.App import zcml
from zope.component.hooks import setHooks

import doctest
import re
import six


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
    placeless.setUp()
    import Products.Five
    from five import intid
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', intid)
    zcml.load_config('test.zcml', intid)
    setHooks()


def tearDown():
    placeless.tearDown()


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            want = re.sub("b'(.*?)'", "'\\1'", want)
        else:
            want = re.sub("u'(.*?)'", "'\\1'", want)
            # translate doctest exceptions
            for dotted in (
                'zope.interface.interfaces.ComponentLookupError',
                'zope.keyreference.interfaces.NotYet',
                'zope.intid.interfaces.IntIdMissingError',
                'zope.intid.interfaces.ObjectMissingError',
            ):
                if dotted in got:
                    got = re.sub(
                        dotted,
                        dotted.rpartition('.')[-1],
                        got,
                    )
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    import unittest
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    return unittest.TestSuite([
        FunctionalDocFileSuite(
            'README.rst',
            package='five.intid',
            optionflags=optionflags,
            checker=Py23DocChecker(),
        )
    ])
