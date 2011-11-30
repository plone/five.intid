# Sometimes persistent classes are never meant to be persisted. The most
# common example are CMFCore directory views and filesystem objects.
# Register specific handlers that are no-ops to circumvent
from five.intid.keyreference import KeyReferenceToPersistent
from zope.interface import implements
from zope.keyreference.interfaces import IKeyReference, NotYet
from Products.CMFCore.utils import getToolByName


def addIntIdSubscriber(ob, event):
    return

def removeIntIdSubscriber(ob, event):
    return

def moveIntIdSubscriber(ob, event):
    return

class KeyReferenceNever(object):
    """A keyreference that is never ready"""
    implements(IKeyReference)

    key_type_id = 'five.intid.cmfexceptions.keyreference'

    def __init__(self, obj):
        raise NotYet()

    def __call__(self):
        return None

    def __cmp__(self, other):
        if self.key_type_id == other.key_type_id:
            return cmp(self, other)
        return cmp(self.key_type_id, other.key_type_id)


class NoTemporaryKeyReference(KeyReferenceToPersistent):
    """A keyreference that never accepts objects in the portal_factory"""
    implements(IKeyReference)

    def __init__(self, wrapped_obj):
        factorytool = getToolByName(wrapped_obj, 'portal_factory', None)
        if factorytool is not None:
            if factorytool.isTemporary(wrapped_obj):
                raise NotYet()
        super(NoTemporaryKeyReference, self).__init__(wrapped_obj)
