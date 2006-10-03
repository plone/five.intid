from Acquisition import aq_parent
from Products.Five import BrowserView
from Products.Five.site.localsite import enableLocalSiteHook, disableLocalSiteHook
from zope.app.component.hooks import setSite, setHooks
from zope.app.component.interfaces import ISite
from zope.component.interfaces import ComponentLookupError
from zope.component import getUtility
from OFS.interfaces import IApplication
from intid import IIntIds, OFSIntIds

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
        addUtility(self.context, IIntIds, OFSIntIds, findroot=False)

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
    enableLocalSiteHook(site)
    if sethook:
         setHooks()
    setSite(site)

def get_root(app):
    # adapted from alecm's 'listen'
    while app is not None and not IApplication.providedBy(app):
            app = aq_parent(app)
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
        sm.registerUtility(interface, obj, name=name)  #2.9

from intid import IIntIds, OFSIntIds
from zope.component import getUtility

def add_intids(site, findroot=False):
    addUtility(site, IIntIds, OFSIntIds, findroot=findroot)

def get_intids(context=None):
    return getUtility(IIntIds, context=context)

def del_intids(context=None, findroot=False):
    if findroot:
        context = get_root(context)
    utility = get_intids(context)
    parent = utility.aq_parent
    parent.manage_delObjects([utility.getId()])
    
