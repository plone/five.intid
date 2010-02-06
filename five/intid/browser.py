from zope.app.intid.browser import IntIdsView
from Products.Five import BrowserView

class FiveIntIdsView(IntIdsView, BrowserView):
    """ utility view for five """
