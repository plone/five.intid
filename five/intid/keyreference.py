from Acquisition import IAcquirer, aq_base
from ZODB.interfaces import IConnection
from persistent import IPersistent
from zope.component import adapter, adapts
from zope.interface import implements, implementer
from zope.app.keyreference.interfaces import IKeyReference, NotYet
from zope.app.keyreference.persistent import KeyReferenceToPersistent

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

    def __init__(self, object):
        if not getattr(object, '_p_oid', None):
            connection = IConnection(object, None)
            if connection is None:
                raise NotYet(object)
            connection.add(object)
        object = aq_base(object)
        self.object = object
