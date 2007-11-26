from Acquisition import aq_base, aq_inner, IAcquirer

marker = object()
def test_settable(obj, attr):
    """
    simple test to make sure an attr on an object is settable.

    Use to avoid CMF __setattr__ hacks.

    >>> readonly = tuple()
    >>> test_settable(readonly, '_p_oid')
    False

    >>> writeable = type('writeable', (object,), {})()
    >>> test_settable(writeable, '_p_oid')
    True

    No new attributes should be added
    >>> hasattr(writeable, '_p_oid')
    False

    All existing attrs should remain the same

    >>> writeable._p_oid='xxxxxx'
    >>> test_settable(writeable, '_p_oid')
    True

    >>> writeable._p_oid=='xxxxxx'
    True
    """

    settable = False
    orig = marker
    if hasattr(obj, attr):
        orig = getattr(obj, attr, None)

    try:
        setattr(obj, attr, marker)
    except AttributeError:
        return False
    
    if getattr(obj, attr, None) is marker:
        settable = True
        if orig is marker:
            delattr(obj, attr)
        else:
            setattr(obj, attr, orig)
    return settable

def aq_iter(obj, error=None):
    if not (IAcquirer.providedBy(obj) or hasattr(obj, '__parent__')):
        raise TypeError("%s not acquisition wrapped" %obj)

    # adapted from alecm's 'listen'
    seen = set()
    # get the inner-most wrapper (maybe save some cycles, and prevent
    # bogus loop detection)
    cur = aq_inner(obj)
    while cur is not None:
        yield cur
        seen.add(id(aq_base(cur)))
        cur = getattr(cur, 'aq_parent', getattr(cur, '__parent__', None))
        if id(aq_base(cur)) in seen:
            # avoid loops resulting from acquisition-less views
            # whose __parent__ points to
            # the context whose aq_parent points to the view
            if error is not None:
                raise error, '__parent__ loop found'
            break

