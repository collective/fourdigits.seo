from cgi import escape
from fourdigits.seo.behaviors.seo import ISeoAdapter
from fourdigits.seo.browser.settings import ISeoSettings
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from DateTime import DateTime
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import getExprContext


class PropertiesBase(BrowserView):
    def __call__(self):
        self.properties = []
        adapted = ISeoAdapter(self.context)
        self.title = adapted.title
        self.description = adapted.description
        registry = getUtility(IRegistry)
        self.seoSettings = registry.forInterface(ISeoSettings)
        mtool = getToolByName(self.context, 'portal_membership')
        self.member = mtool.getMemberById(self.context.Creator())
        self.image = getattr(self.context, 'image',
                             getattr(self.context, 'afbeelding', None))
        if getattr(self.context, 'image', None):
            self.imagename = 'image'
        elif getattr(self.context, 'afbeelding', None):
            self.imagename = 'afbeelding'

    def getScale(self, width=None, height=None):
        try:
            scales = self.context.restrictedTraverse('@@images')
            scale = scales.scale(self.imagename, width=width, height=height)
        except AttributeError:
            scale = False

        return scale


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
            thumbnail = self.getScale(width=120, height=120)
            if thumbnail:
                self.properties.append(('twitter:image', thumbnail.url))

        return self.properties


class TwitterCardPhoto(TwitterBase):
    def __call__(self):
        super(TwitterCardPhoto, self).__call__()
        self.properties.append(('twitter:card', 'photo'))

        if self.image:
            thumbnail = self.getScale(width=560, height=750)
            if thumbnail:
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
            large = self.getScale(width=1000, height=1000)
            if large:
                self.properties.append(('og:image', large.url))
                self.properties.append(('og:image:type',
                                        self.image.contentType))
                self.properties.append(('og:image:width', large.width))
                self.properties.append(('og:image:height', large.height))
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
        if '_' not in loc:
            # make sure its nl_NL or en_US
            loc = loc.lower() + '_' + loc.upper()
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

        if self.member:
            if self.member.getProperty('first_name') and \
                    self.seoSettings.exposeAuthorOpenGraph:
                self.properties.append(('og:article:author:first_name',
                                        self.member.getProperty('first_name')))

            if self.member.getProperty('last_name') and \
                    self.seoSettings.exposeAuthorOpenGraph:
                self.properties.append(('og:article:author:last_name',
                                        self.member.getProperty('last_name')))

            if self.member.getProperty('id') and \
                    self.seoSettings.exposeAuthorOpenGraph:
                self.properties.append(('og:article:author:username',
                                        self.member.getProperty('id')))

            if self.member.getProperty('gender') and \
                    self.seoSettings.exposeAuthorOpenGraph:
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


class Sitemap(BrowserView):
    index = ViewPageTemplateFile("templates/sitemap.pt")

    def render(self):
        return self.index()

    def results(self):
        objects = []

        def recurse(context):
            lastmod = None
            default_page = getattr(context.aq_base, 'default_page', False)
            portal_type = getattr(context.aq_base, 'portal_type', False)
            noindex = False

            if default_page:
                lastmod = context[default_page].modified()
                noindex = getattr(context[default_page].aq_base,
                                  'seo_noindex', False) or \
                          getattr(context.aq_base, 'seo_noindex', False)
            else:
                lastmod = context.modified()
                noindex = getattr(context.aq_base, 'seo_noindex', False)

            if not noindex and portal_type != 'Image':
                objects.append({
                    'url': context.absolute_url(),
                    'lastmod': DateTime(lastmod).HTML4()
                })

            if IFolderish.providedBy(context):
                for id, item in context.contentItems():
                    recurse(item)

        recurse(self.context)

        return objects

    def __call__(self):
        return self.render()


class SitemapImage(BrowserView):
    index = ViewPageTemplateFile("templates/sitemap-image.pt")

    def render(self):
        return self.index()

    def portal_url(self):
        return self.context.absolute_url()

    def results(self):
        objects = []
        images = self.context.portal_catalog(portal_type = ['Image', ])

        for image in images:
            obj = image.getObject()
            if not getattr(obj, 'seo_noindex', False):
                objects.append({
                    'url': obj.absolute_url(),
                    'title': obj.Title()
                })

        return objects

    def __call__(self):
        return self.render()