from Acquisition import IAcquirer, aq_base, ImplicitAcquisitionWrapper
from ZODB.interfaces import IConnection
from persistent import IPersistent
from zope.component import adapter, adapts
from zope.interface import implements, implementer
from zope.app.keyreference.interfaces import IKeyReference, NotYet
from zope.app.keyreference.persistent import KeyReferenceToPersistent
from site import get_root
from utils import test_settable
from interfaces import UnsettableAttributeError
from zope.app.container.interfaces import IObjectAddedEvent

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

@adapter(IPersistent, IObjectAddedEvent)
def add_object_to_connection(ob, event):
    """ a salve for screwy CMF behavior """
    connection = IConnection(ob, None)
    if None is not connection:
        connection.add(aq_base(ob))


class KeyReferenceToPersistent(KeyReferenceToPersistent):
    """a zope2ish implementation of keyreferences that unwraps objects
    that have Acquisition wrappers

    These references compare by _p_oids of the objects they reference.

    @@ cache IConnection as a property and volative attr?
    """
    implements(IKeyReference)
    adapts(IPersistent)

    key_type_id = 'five.intid.keyreference'

    def __init__(self, wrapped_obj):
        self.path = '/'.join(wrapped_obj.getPhysicalPath())
        self.object = aq_base(wrapped_obj)
        connection = IConnection(wrapped_obj, None)

        if not getattr(self.object, '_p_oid', None):
            if connection is None:
                raise NotYet(wrapped_obj)

            # DirectoryViews do not allow setting of _p_oid
            # will cause transaction errors
            if not test_settable(self.object, '_p_oid'):
                raise UnsettableAttributeError(wrapped_obj)
            connection.add(self.object)

        self.root_oid = get_root(wrapped_obj)._p_oid            
        self.oid = self.object._p_oid
        self.dbname = connection.db().database_name

    @property
    def root(self):
        return IConnection(self.object)[self.root_oid]

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
            try:
                other = (IConnection(other.object).db().database_name, other.object._p_oid)
            except TypeError:
                other = None
            return cmp(
                (IConnection(self.object).db().database_name,  self.object._p_oid),
                other,
                )

        return cmp(self.key_type_id, other.key_type_id)
