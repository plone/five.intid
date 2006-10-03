============
 Five IntId
============

This is a compatibility layer for zope.app.intid(and consequentually,
zope.app.keyreferences)

First, let make sure the ofs utility is provides the interface::

    >>> from zope.app.intid.interfaces import IIntIds
    >>> from five.intid.intid import OFSIntIds
    
    #>>> zope.interface.verifyObject(IIntIds, OFSIntIds()) # verifyObject broken?

Content added before the utility won't be registered(until explicitly
called to). We'll set some up now for later

    >>> manage_addSimpleContent(self.folder, 'mycont1', "My Content")
    >>> content1 = self.folder.mycont1

`five.intid.site` has convenience functions for adding, get and
removing an IntId utility: `add_intid`, `get_intid`, `del_intid`.

Adding::

    >>> from five.intid.site import add_intids, get_intids, del_intids
    >>> add_intids(self.folder)
    >>> self.folder.utilities.IIntIds
    <OFSIntIds at /test_folder_1_/utilities/IIntIds>

You can also tell `add_intids` to find the site root, and install there::

    >>> add_intids(self.folder, findroot=True)
    >>> self.app.utilities.IIntIds
    <OFSIntIds at /utilities/IIntIds>

To get a local intid utility::

    >>> site.get_intids(self.folder)
    <OFSIntIds at /test_folder_1_/utilities/IIntIds>
    
    >>> site.get_intids(self.app)
    <OFSIntIds at /utilities/IIntIds>

And finally, do a remove::

    >>> site.del_intids(self.folder, findroot=True)
    >>> self.app.utilities.objectIds()
    []

Before we look at intid events, we need to set the traversal
hook. Once we have done this, when we ask for all registered Intids,
we will get the utility from test folder::

    >>> setSite(self.folder)
    >>> tuple(zope.component.getAllUtilitiesRegisteredFor(IIntIds))
    (<OFSIntIds at /test_folder_1_/utilities/IIntIds>,)


When we add content, event will be fired to add keyreference for said
objects the utilities (currently, our content and the utility are
registered)::

    >>> manage_addSimpleContent(self.folder, 'mycont2', "My Content")
    >>> content2 = self.folder.mycont2
    >>> intid = site.get_intids(self.folder)
    >>> len(intid.items())
    2

Pre-existing content will raise a keyerror if passed to the intid
utility::

    >>> intid.getId(content1)
    Traceback (most recent call last):
    ...
    KeyError: <SimpleContent at /test_folder_1_/mycont1>

We can call the keyreferences, and get the objects back::

    >>> intid.items()[0][1]()
    <OFSIntIds at /test_folder_1_/utilities/IIntIds>

    >>> intid.items()[1][1]()
    <SimpleContent at /test_folder_1_/mycont2>

we can get an object's `intid` from the utility like so::

    >>> ob_id = intid.getId(content2)

and get an object back like this::

    >>> intid.getObject(ob_id)
    <SimpleContent at /test_folder_1_/mycont2>

these objects are aquisition wrapped on retrieval::

    >>> type(intid.getObject(ob_id))
    <type 'ImplicitAcquirerWrapper'>

When an object is added or removed, subscribers add it to the intid
utility, and fire an event is fired
(zope.app.intid.interfaces.IIntIdAddedEvent,
zope.app.intid.interfaces.IIntIdRemovedEvent respectively).

`five.intid` hooks up these events to redispatch as object events. The
tests hook up a simple subscriber to verify that the intid object
events are fired (these events are useful for catalogish tasks). 

    >>> import five.intid.tests as tests
    >>> tests.NOTIFIED[0]
    '<SimpleContent at mycont2> <...IntIdAddedEvent instance at ...'

Registering and unregistering objects does not fire these events::

    >>> tests.NOTIFIED[0] = "No change"
    >>> uid = intid.register(content1)
    >>> intid.getObject(uid)
    <SimpleContent at /test_folder_1_/mycont1>

    >>> tests.NOTIFIED[0]
    'No change'

    >>> intid.unregister(content1)
    >>> intid.getObject(uid)
    Traceback (most recent call last):
    ...
    KeyError: ...

    >>> tests.NOTIFIED[0]
    'No change'

This is a good time to take a look at keyreferences, the core part of
this system.


Key References in Zope2
=======================

Key references are hashable objects returned by IKeyReference.  The
hash produced is a unique identifier for whatever the object is
referencing(another zodb object, a hook for sqlobject, etc)::

object retrieval in intid occurs by calling a key reference. This
implementation is slightly different than the zope3 due to
acquistion.

The factories returned by IKeyReference must persist and this dictates
being especially careful about references to acquisition wrapped
objects as well as return acq wrapped objects as usually expected in
zope2.

    >>> ref = intid.refs[ob_id]
    >>> ref
    <five.intid.keyreference.KeyReferenceToPersistent object at ...>

The reference object holds a reference to the unwrapped target object
and a property to fetch the app(also, not wrapped ie <type 'ImplicitAcquirerWrapper'>)::

    >>> ref.object
    <SimpleContent at mycont2>

    >>> type(ref.object)
    <class 'Products.Five.tests.testing.simplecontent.SimpleContent'>
 
    >>> ref.root
    <Application at >

Calling the reference object (or the property wrapped_object) will
return an acquisition object wrapped object (wrapped as it was
created)::

    >>> ref.wrapped_object == ref()
    True
    
    >>> ref()
    <SimpleContent at /test_folder_1_/mycont2>
    
    >>> type(ref())
    <type 'ImplicitAcquirerWrapper'>

The hash calculation is a combination of the database name and the
object's persistent object id(oid)::

    >>> ref.dbname
    'unnamed'

    >>> hash((ref.dbname, ref.object._p_oid)) == hash(ref)
    True

