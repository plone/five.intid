# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import IAcquirer


def aq_iter(obj, error=None):
    if not (IAcquirer.providedBy(obj) or hasattr(obj, '__parent__')):
        raise TypeError("%s not acquisition wrapped" % obj)

    # adapted from alecm's 'listen'
    seen = set()
    # get the inner-most wrapper (maybe save some cycles, and prevent
    # bogus loop detection)
    cur = aq_inner(obj)
    while cur is not None:
        yield cur
        seen.add(id(aq_base(cur)))
        cur = getattr(cur, 'aq_parent', getattr(cur, '__parent__', None))
        if cur:
            cur = aq_inner(cur)  # unwrap from Acquisition context
        if id(aq_base(cur)) in seen:
            if error is not None:
                raise error('__parent__ loop found')
            break
