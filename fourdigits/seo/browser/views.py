from Products.Five import BrowserView
from fourdigits.seo.behaviors.seo import ISeoAdapter
from cgi import escape
from plone.registry.interfaces import IRegistry
from fourdigits.seo.browser.settings import ISeoSettings
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class PropertiesBase(BrowserView):
    def __call__(self):
        self.properties = []
        adapted = ISeoAdapter(self.context)
        self.title = escape(adapted.title)
        self.description = escape(adapted.description)
        registry = getUtility(IRegistry)
        self.seoSettings = registry.forInterface(ISeoSettings)
        mtool = getToolByName(self.context, 'portal_membership')
        self.member = mtool.getMemberById(self.context.Creator())


class TwitterBase(PropertiesBase):
    def __call__(self):
        super(TwitterBase, self).__call__()
        self.properties.append(('twitter:title', self.title))
        self.properties.append(('twitter:description', self.description))

        if self.seoSettings.twitterSiteAccount:
            self.properties.append(('twitter:site',
                                    self.seoSettings.twitterSiteAccount))

        if self.member and self.member.getProperty('twitter_author', False):
            self.properties.append(('twitter:creator',
                                    self.member.getProperty('twitter_author')))


class TwitterCardSummary(TwitterBase):
    def __call__(self):
        super(TwitterCardSummary, self).__call__()
        self.properties.append(('twitter:card', 'summary'))

        # self.properties.append(('twitter:image', ''))

        return self.properties


class OpenGraphBase(PropertiesBase):
    def __call__(self):
        super(OpenGraphBase, self).__call__()
        self.properties.append(('og:title', self.title))
        self.properties.append(('og:description', self.description))

        # self.properties.append(('og:image', ''))

        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        canonical_url = context_state.canonical_object_url()
        self.properties.append(('og:url', canonical_url))

        portal_properties = getToolByName(self.context, 'portal_properties')
        loc = portal_properties.site_properties.getProperty('default_language')
        if '-' in loc:
            loc = loc.split('-')[0] + '_' + loc.split('-')[1].upper()
        self.properties.append(('og:locale', loc))


class OpenGraphArticle(OpenGraphBase):
    def __call__(self):
        super(OpenGraphArticle, self).__call__()
        self.properties.append(('og:type', 'article'))

        return self.properties
