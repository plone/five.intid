from Acquisition import IAcquirer, aq_base, ImplicitAcquisitionWrapper
from ZODB.interfaces import IConnection
from persistent import IPersistent
from zope.component import adapter, adapts
from zope.interface import implements, implementer
from zope.app.keyreference.interfaces import IKeyReference, NotYet
from zope.app.keyreference.persistent import KeyReferenceToPersistent
from site import get_root

@adapter(IPersistent)
@implementer(IConnection)
def connectionOfPersistent(obj):
    """ zope2 cxn fetcher for wrapped items """
    cur = obj
    if IAcquirer.providedBy(obj):
        while not getattr(cur, '_p_jar', None):
            cur = getattr(cur, 'aq_parent', None)
            if cur is None:
                return None
        return cur._p_jar
    else:
        raise TypeError("%s not acquisition wrapped" %obj)


class KeyReferenceToPersistent(KeyReferenceToPersistent):
    """a zope2ish implementation of keyreferences that unwraps objects
    that have Acquisition wrappers

    These references compare by _p_oids of the objects they reference.
    """
    implements(IKeyReference)
    adapts(IPersistent)

    key_type_id = 'five.intid.keyreference'

    def __init__(self, wrapped_obj):
        self.path = '/'.join(wrapped_obj.getPhysicalPath())
        self.object = aq_base(wrapped_obj)
        if not getattr(self.object, '_p_oid', None):
            connection = IConnection(wrapped_obj, None)
            if connection is None:
                raise NotYet(wrapped_object)
            connection.add(self.object)
        self.root_oid = get_root(wrapped_obj)._p_oid            
        del wrapped_obj            

        self.oid = self.object._p_oid
        self.dbname = self.object._p_jar.db().database_name

    @property
    def root(self):
        return self.object._p_jar[self.root_oid]

    @property
    def wrapped_object(self):
        return self.root.restrictedTraverse(self.path)
    
    def __call__(self):
        return self.wrapped_object
        
    def __hash__(self):
        return hash((self.dbname,
                     self.object._p_oid,
                     ))

    def __cmp__(self, other):
        if self.key_type_id == other.key_type_id:
            return cmp(
                (self.object._p_jar.db().database_name,  self.object._p_oid),
                (other.object._p_jar.db().database_name, other.object._p_oid),
                )

        return cmp(self.key_type_id, other.key_type_id)
