# -*- coding: utf-8 -*-
# Sometimes persistent classes are never meant to be persisted. The most
# common example are CMFCore directory views and filesystem objects.
# Register specific handlers that are no-ops to circumvent
from zope.interface import implementer
from zope.keyreference.interfaces import IKeyReference
from zope.keyreference.interfaces import NotYet


def addIntIdSubscriber(ob, event):
    return


def removeIntIdSubscriber(ob, event):
    return


def moveIntIdSubscriber(ob, event):
    return


@implementer(IKeyReference)
class KeyReferenceNever(object):
    """A keyreference that is never ready"""

    key_type_id = 'five.intid.cmfexceptions.keyreference'

    def __init__(self, obj):
        raise NotYet()

    def __call__(self):
        return None

    def __cmp__(self, other):
        if self.key_type_id == other.key_type_id:
            return cmp(self, other)
        return cmp(self.key_type_id, other.key_type_id)
