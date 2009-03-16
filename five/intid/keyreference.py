from Acquisition import aq_base, aq_chain
from ZODB.interfaces import IConnection
from ZPublisher.BaseRequest import RequestContainer
from zExceptions import NotFound
from persistent import IPersistent
from zope.component import adapter, adapts
from zope.app.component.hooks import getSite
from zope.interface import implements, implementer
from zope.app.keyreference.interfaces import IKeyReference, NotYet
from zope.app.keyreference.persistent import KeyReferenceToPersistent
from site import get_root, aq_iter
from zope.app.container.interfaces import IObjectAddedEvent


@adapter(IPersistent)
@implementer(IConnection)
def connectionOfPersistent(obj):
    """ zope2 cxn fetcher for wrapped items """
    for parent in aq_iter(obj):
        conn = getattr(parent, '_p_jar', None)
        if conn is not None:
            return conn


@adapter(IPersistent, IObjectAddedEvent)
def add_object_to_connection(ob, event):
    """Pre-add new objects to their persistence connection"""
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
        # make sure our object is wrapped by containment only
        try:
            self.path = '/'.join(wrapped_obj.getPhysicalPath())
        except AttributeError:
            self.path = None
        
        # If the path ends with /, it means the object had an empty id.
        # This means it's not yet added to the container, and so we have
        # to defer.
        if self.path is not None and self.path.endswith('/'):
            raise NotYet(wrapped_obj)
        self.object = aq_base(wrapped_obj)
        connection = IConnection(wrapped_obj, None)

        if not getattr(self.object, '_p_oid', None):
            if connection is None:
                raise NotYet(wrapped_obj)
            connection.add(self.object)
        
        try:
            self.root_oid = get_root(wrapped_obj)._p_oid
        except AttributeError:
            # If the object is unwrapped we can try to use the Site from the
            # threadlocal as our acquisition context, hopefully it's not
            # something odd.
            self.root_oid = get_root(getSite())._p_oid
        self.oid = self.object._p_oid
        self.dbname = connection.db().database_name

    @property
    def root(self):
        return IConnection(self.object)[self.root_oid]

    @property
    def wrapped_object(self):
        if self.path is None:
            return self.object
        try:
            obj = self.root.unrestrictedTraverse(self.path)
        except NotFound:
            return self.object
        chain = aq_chain(obj)
        # Try to ensure we have a request at the acquisition root
        # by using the one from getSite
        if not len(chain) or not isinstance(chain[-1], RequestContainer):
            site = getSite()
            site_chain = aq_chain(site)
            if len(site_chain) and isinstance(site_chain[-1],
                                              RequestContainer):
                req = site_chain[-1]
                new_obj = req
                # rebuld the chain with the request at the bottom
                for item in reversed(chain):
                    new_obj = aq_base(item).__of__(new_obj)
                obj = new_obj
        return obj

    def __call__(self):
        return self.wrapped_object

    def __hash__(self):
        return hash((self.dbname,
                     self.object._p_oid,
                     ))

    def __cmp__(self, other):
        if self.key_type_id == other.key_type_id:
            return cmp((self.dbname,self.oid), (other.dbname, other.oid))
        return cmp(self.key_type_id, other.key_type_id)
