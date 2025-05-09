from AccessControl.class_init import InitializeClass
from Acquisition import Explicit
from zope.component import getAllUtilitiesRegisteredFor
from zope.event import notify
from zope.interface import implementer
from zope.intid import IntIds as z3IntIds
from zope.intid.interfaces import IIntIds
from zope.intid.interfaces import IntIdAddedEvent
from zope.intid.interfaces import IntIdRemovedEvent
from zope.keyreference.interfaces import IKeyReference
from zope.keyreference.interfaces import NotYet


_marker = []


@implementer(IIntIds)
class IntIds(z3IntIds):
    """zope2ish intid utility"""

    meta_type = "IntId Utility"

    def __init__(self, id_=IIntIds.__name__):
        self.id = self.__name__ = id_
        super().__init__()

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


# BBB
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
    utilities = tuple(getAllUtilitiesRegisteredFor(IIntIds))
    if utilities:  # assert that there are any utilities
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
    utilities = tuple(getAllUtilitiesRegisteredFor(IIntIds))
    if not utilities:
        return
    try:
        key = IKeyReference(ob, None)
    except NotYet:
        key = None

    # Register only objects that adapt to key reference
    if key is None:
        return

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
    utilities = tuple(getAllUtilitiesRegisteredFor(IIntIds))
    if not utilities:
        return
    try:
        key = IKeyReference(ob, None)
    except NotYet:
        key = None

    # Register only objects that adapt to key reference
    if key is None:
        return

    # Update objects that adapt to key reference
    for utility in utilities:
        try:
            uid = utility.getId(ob)
            # XXX this is a temporary workaround
            utility.refs.pop(uid, None)
            utility.ids.pop(key, None)
            utility.refs[uid] = key
            utility.ids[key] = uid
        except KeyError:
            pass
