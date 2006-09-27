from zope.app.intid import IntIds
from OFS.SimpleItem import SimpleItem
from zope.app.intid.interfaces import IIntIds
from zope.interface import implements

class OFSIntIds(IntIds, SimpleItem):
    """ zope2ish intid utility """
    implements(IIntIds)
    
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
