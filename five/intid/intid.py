from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from zope.app import zapi
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.intid.interfaces import IntIdAddedEvent, IntIdRemovedEvent
from zope.app.keyreference.interfaces import IKeyReference, NotYet
from zope.event import notify
from zope.interface import implements

class OFSIntIds(SimpleItem, IntIds):
    """ zope2ish intid utility """
    implements(IIntIds)

    meta_type="IntId Utility"

    def __init__(self, id_=IIntIds.__name__):
        self.id = id_
        super(OFSIntIds, self).__init__()

    def getId(*args):
        # sweet compatibility
        if len(args) == 1:
            return SimpleItem.getId(args[0])
        return IntIds.getId(*args)
    
    def register(self, ob):
        key = IKeyReference(ob)
        if key in self.ids:
            return self.ids[key]
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
        try:
            key = IKeyReference(ob, None)
        except NotYet:
            key = None
            
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
        try:
            key = IKeyReference(ob, None)
        except NotYet:
            key = None
            
        # Register only objects that adapt to key reference
        if key is not None:
            # Notify the catalogs that this object is about to be removed.
            notify(IntIdRemovedEvent(ob, event))
            for utility in utilities:
                try:
                    utility.unregister(key)
                except KeyError:
                    pass
