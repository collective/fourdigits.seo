from cgi import escape
from fourdigits.seo.behaviors.seo import ISeoAdapter
from fourdigits.seo.browser.settings import ISeoSettings
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import getExprContext


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
        self.image = getattr(self.context, 'image', None)


class TwitterBase(PropertiesBase):
    def __call__(self):
        super(TwitterBase, self).__call__()
        self.properties.append(('twitter:title', self.title))

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

        self.properties.append(('twitter:description', self.description))

        if self.image:
            scales = self.context.restrictedTraverse('@@images')
            thumbnail = scales.scale('image', width=120, height=120,
                                     direction="down")
            self.properties.append(('twitter:image', thumbnail.url))

        return self.properties


class TwitterCardPhoto(TwitterBase):
    def __call__(self):
        super(TwitterCardPhoto, self).__call__()
        self.properties.append(('twitter:card', 'photo'))

        if self.image:
            scales = self.context.restrictedTraverse('@@images')
            thumbnail = scales.scale('image', width=560, height=750)
            self.properties.append(('twitter:image', thumbnail.url))
            self.properties.append(('twitter:image:width', thumbnail.width))
            self.properties.append(('twitter:image:height', thumbnail.height))

        return self.properties


class OpenGraphBase(PropertiesBase):
    def __call__(self):
        super(OpenGraphBase, self).__call__()
        self.properties.append(('og:title', self.title))
        self.properties.append(('og:description', self.description))

        if self.image:
            self.properties.append(('og:image', self.context.absolute_url()))
            self.properties.append(('og:image:type', self.image.contentType))
            self.properties.append(('og:image:width', self.image._width))
            self.properties.append(('og:image:height', self.image._height))
        elif self.seoSettings.openGraphFallbackImage:
            expression = Expression(
                str(self.seoSettings.openGraphFallbackImage))
            expression_context = getExprContext(self.context)
            self.properties.append(('og:image',
                                    expression(expression_context)))

        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        canonical_url = context_state.canonical_object_url()
        self.properties.append(('og:url', canonical_url))

        portal_properties = getToolByName(self.context, 'portal_properties')
        loc = portal_properties.site_properties.getProperty('default_language')
        if '-' in loc:
            loc = loc.split('-')[0] + '_' + loc.split('-')[1].upper()
        self.properties.append(('og:locale', loc))

        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        portal_title = escape(safe_unicode(self.portal_state
                                           .navigation_root_title()))
        self.properties.append(('og:site_name', portal_title))


class OpenGraphArticle(OpenGraphBase):
    def __call__(self):
        super(OpenGraphArticle, self).__call__()
        self.properties.append(('og:type', 'article'))

        if self.context.EffectiveDate() != 'None':
            self.properties.append(('og:article:published_time',
                                    self.context.effective_date.ISO8601()))

        self.properties.append(('og:article:modified_time',
                                self.context.modified().ISO8601()))

        if self.context.ExpirationDate() != 'None':
            self.properties.append(('og:article:expiration_time',
                                    self.context.expiration_date.ISO8601()))

        if self.member.getProperty('first_name'):
            self.properties.append(('og:article:author:first_name',
                                    self.member.getProperty('first_name')))

        if self.member.getProperty('last_name'):
            self.properties.append(('og:article:author:last_name',
                                    self.member.getProperty('last_name')))

        if self.member.getProperty('id'):
            self.properties.append(('og:article:author:username',
                                    self.member.getProperty('id')))

        if self.member.getProperty('gender'):
            self.properties.append(('og:article:author:gender',
                                    self.member.getProperty('gender')))

        navroot = self.portal_state.navigation_root()
        contentPath = self.context.getPhysicalPath()[
            len(navroot.getPhysicalPath()):]
        if contentPath:
            self.properties.append(('og:article:section',
                                    navroot[contentPath[0]].Title()))

        for tag in self.context.Subject():
            self.properties.append(('og:article:tag', escape(tag)))

        return self.properties


class OpenGraphWebsite(OpenGraphBase):
    def __call__(self):
        super(OpenGraphWebsite, self).__call__()
        self.properties.append(('og:type', 'website'))

        return self.properties
