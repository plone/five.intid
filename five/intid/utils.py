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
