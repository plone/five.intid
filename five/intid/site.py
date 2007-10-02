from Acquisition import aq_parent, aq_base, aq_inner
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
        addUtility(self.context, IIntIds, findroot=False)

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
    # adapted from alecm's 'listen'
    seen = {}
    # get the inner-most wrapper (maybe save some cycles, and prevent
    # bogus loop detection)
    app = aq_inner(app)
    while app is not None and not IApplication.providedBy(app):
        seen[id(aq_base(app))] = 1
        app = getattr(app, 'aq_parent', getattr(app, '__parent__', None))
        if id(aq_base(app)) in seen:
            # avoid loops resulting from acquisition-less views
            # whose __parent__ points to
            # the context whose aq_parent points to the view
            raise AttributeError, '__parent__ loop found'
    if app is None:
        raise AttributeError, 'No application found'
    return app

def addUtility(site, interface, klass, name='', findroot=True):
    """
    add local utility in zope2
    """
    app = site
    if findroot:
        app = get_root(site)

    # If we have the zope Application and the utility is not yet
    # registered, then register it.
    assert app, TypeError("app is None")

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
