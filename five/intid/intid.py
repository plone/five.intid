from zope.app.intid import IntIds
from OFS.SimpleItem import SimpleItem
from zope.app.intid.interfaces import IIntIds
from zope.interface import implements
from zope.app.keyreference.interfaces import IKeyReference

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
