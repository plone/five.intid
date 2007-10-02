"""
five.localsitemanager/PersistentComponents compatibility support.
"""

try:
    from five.localsitemanager import (
        make_objectmanager_site as make_site, )
except ImportError:
    USE_LSM = False
    from Products.Five.site.localsite import (
        enableLocalSiteHook as make_site, )
else:
    USE_LSM = True
