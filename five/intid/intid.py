try:
    from App.class_init import InitializeClass
except ImportError:
    # BBB Zope < 2.12
    from Globals import InitializeClass
from persistent import Persistent
from Acquisition import Explicit
from zope.app import zapi
from zope.app.intid import IntIds as z3IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.intid.interfaces import IntIdAddedEvent, IntIdRemovedEvent
from zope.app.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent
from zope.app.keyreference.interfaces import IKeyReference, NotYet
from zope.event import notify
from zope.interface import implements

_marker = []

class IntIds(z3IntIds):
    """ zope2ish intid utility """
    implements(IIntIds)

    meta_type="IntId Utility"

    def __init__(self, id_=IIntIds.__name__):
        self.id = self.__name__ = id_
        super(IntIds, self).__init__()

    def getId(self, ob=_marker):
        # Compatibility with SimpleItem
        if ob is _marker:
            return self.__name__
        return z3IntIds.getId(self, ob)

    def register(self, ob):
        key = IKeyReference(ob)
        res = self.ids.get(key, None)
        if res is not None:
            return res
        uid = self._generateId()
        self.refs[uid] = key
        self.ids[key] = uid
        return uid

    def unregister(self, ob):
        key = IKeyReference(ob, None)
        if key is None:
            return

        uid = self.ids[key]
        del self.refs[uid]
        del self.ids[key]

InitializeClass(IntIds)

class OFSIntIds(IntIds, Explicit):
    """Mixin acquisition for non-lsm sites"""

    def manage_fixupOwnershipAfterAdd(self):
        pass
    def wl_isLocked(self):
        return False

InitializeClass(OFSIntIds)

# @@ these are "sloppy" subscribers that let objects that have not
# been properly added to the db by
def addIntIdSubscriber(ob, event):
    """A subscriber to ObjectAddedEvent

    Registers the object added in all unique id utilities and fires
    an event for the catalogs.
    """
    utilities = tuple(zapi.getAllUtilitiesRegisteredFor(IIntIds))
    if utilities: # assert that there are any utilites
        key = None
        try:
            key = IKeyReference(ob, None)
        except NotYet:
            pass

        # Register only objects that adapt to key reference
        if key is not None:
            for utility in utilities:
                utility.register(key)
            # Notify the catalogs that this object was added.
            notify(IntIdAddedEvent(ob, event))

def removeIntIdSubscriber(ob, event):
    """A subscriber to ObjectRemovedEvent

    Removes the unique ids registered for the object in all the unique
    id utilities.
    """
    utilities = tuple(zapi.getAllUtilitiesRegisteredFor(IIntIds))
    if utilities:
        key = None
        try:
            key = IKeyReference(ob, None)
        except NotYet: # @@ temporary fix
            pass

        # Register only objects that adapt to key reference
        if key is not None:
            # Notify the catalogs that this object is about to be removed.
            notify(IntIdRemovedEvent(ob, event))
            for utility in utilities:
                try:
                    utility.unregister(key)
                except KeyError:
                    pass


def moveIntIdSubscriber(ob, event):
    """A subscriber to ObjectMovedEvent

    Updates the stored path for the object in all the unique
    id utilities.
    """
    if IObjectRemovedEvent.providedBy(event) or \
           IObjectAddedEvent.providedBy(event):
        return
    utilities = tuple(zapi.getAllUtilitiesRegisteredFor(IIntIds))
    if utilities:
        key = None
        try:
            key = IKeyReference(ob, None)
        except NotYet: # @@ temporary fix
            pass

        # Update objects that adapt to key reference
        if key is not None:
            for utility in utilities:
                try:
                    uid = utility.getId(ob)
                    utility.refs[uid] = key
                    utility.ids[key] = uid
                except KeyError:
                    pass
