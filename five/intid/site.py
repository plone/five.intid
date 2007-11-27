from Products.Five import BrowserView
from Products.Five.site.localsite import enableLocalSiteHook, disableLocalSiteHook
from zope.app.intid.interfaces import IIntIds
from zope.app.component.hooks import setSite, setHooks
from zope.app.component.interfaces import ISite
from zope.component.interfaces import ComponentLookupError
from zope.component import getUtility, getSiteManager
from OFS.interfaces import IApplication
from intid import IntIds, OFSIntIds
from lsm import make_site, USE_LSM
from utils import aq_iter

class FiveIntIdsInstall(BrowserView):
    @property
    def context(self):
        return self._context[0]

    def __init__(self, context, request):
        self._context = context,
        self.request = request
        doinstall = self.request.get('install', None)
        if doinstall:
            self.install()

    def install(self):
        add_intids(self.context, findroot=False)

    @property
    def installed(self):
        installed = False
        try:
            intids = getUtility(IIntIds)
            if intids:
                installed = True
        except ComponentLookupError, e:
            pass
        return installed

def initializeSite(site, sethook=False, **kw):
    make_site(site)
    if sethook:
         setHooks()
    setSite(site)

def get_root(app):
    for parent in aq_iter(app, error=AttributeError):
        if IApplication.providedBy(parent):
            return parent
    raise AttributeError, 'No application found'

def addUtility(site, interface, klass, name='', findroot=True):
    """
    add local utility in zope2
    """
    app = site
    if findroot:
        app = get_root(site)

    # If we have the zope Application and the utility is not yet
    # registered, then register it.
    assert app is not None, TypeError("app is None")

    if not ISite.providedBy(app):
        initializeSite(app, sethook=False)

    sm = app.getSiteManager()
    if sm.queryUtility(interface,
                       name=name,
                       default=None) is None:

        if name: obj = klass(name)
        else: obj = klass()
        if USE_LSM:
            sm.registerUtility(provided=interface, component=obj,
                               name=name)
        else:
            sm.registerUtility(interface, obj, name=name)

from intid import IIntIds, OFSIntIds
from zope.component import getUtility

def add_intids(site, findroot=False):
    if USE_LSM:
        klass = IntIds
    else:
        klass = OFSIntIds
    addUtility(site, IIntIds, klass, findroot=findroot)

def get_intids(context=None):
    return getUtility(IIntIds, context=context)

def del_intids(context=None, findroot=False):
    if findroot:
        context = get_root(context)
    utility = get_intids(context)
    if USE_LSM:
        getSiteManager(context).unregisterUtility(component=utility,
                                                  provided=IIntIds)
    else:
        parent = utility.aq_parent
        parent.manage_delObjects([utility.__name__])
