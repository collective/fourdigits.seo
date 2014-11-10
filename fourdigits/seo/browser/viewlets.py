from cgi import escape
from plone.app.layout.viewlets.common import TitleViewlet
from plone.memoize.compress import xhtml_compress
from plone.app.layout.viewlets.common import DublinCoreViewlet
from plone.app.layout.links.viewlets import AuthorViewlet
from plone.memoize.view import memoize
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from fourdigits.seo.browser.settings import ISeoSettings
from fourdigits.seo.behaviors.seo import ISeoAdapter
from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import getExprContext
from Products.CMFCore.interfaces import IContentish
from zope.component import getMultiAdapter


class SeoTitleViewlet(TitleViewlet):

    @property
    @memoize
    def page_title(self):
        '''
        Override the pagetitle when seo title is specified
        '''

        published = getattr(self.request, 'PUBLISHED', None)
        obj_id = getattr(published, 'id', '')
        if not obj_id:
            obj_id = self.request.steps[-1].replace('@', '')

        if obj_id == 'contact-info' and self.seoSettings.contactInfoTitle:
            return self.seoSettings.contactInfoTitle
        elif obj_id in ['login', 'login_form'] and \
                self.seoSettings.loginFormTitle:
            return self.seoSettings.loginFormTitle
        elif obj_id == 'register' and self.seoSettings.registerFormTitle:
            return self.seoSettings.registerFormTitle

        adapted = ISeoAdapter(self.context, None)
        if adapted:
            return escape(adapted.title)

        return super(SeoTitleViewlet, self).page_title

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal_title = escape(safe_unicode(portal_state
                                           .navigation_root_title()))
        registry = getUtility(IRegistry)
        self.seoSettings = registry.forInterface(ISeoSettings)
        if self.page_title == portal_title:
            self.site_title = portal_title
        elif self.seoSettings.includeSiteNameInTitle:
            self.site_title = u"%s %s %s" % (
                self.page_title,
                self.seoSettings.siteNameSeparator,
                portal_title)
        else:
            self.site_title = self.page_title


class SeoDublinCoreViewlet(DublinCoreViewlet):
    index = ViewPageTemplateFile('templates/dublin_core.pt')

    def update(self):
        super(SeoDublinCoreViewlet, self).update()

        published = getattr(self.request, 'PUBLISHED', None)
        adapted = ISeoAdapter(self.context, None)
        registry = getUtility(IRegistry)
        seoSettings = registry.forInterface(ISeoSettings)
        obj_id = getattr(published, 'id', '')
        if not obj_id:
            obj_id = self.request.steps[-1].replace('@', '')

        if obj_id == 'contact-info':
            if seoSettings.contactInfoDescription:
                self.metatags.append(('description',
                                      seoSettings.contactInfoDescription))
        elif obj_id in ['login', 'login_form']:
            if seoSettings.loginFormDescription:
                self.metatags.append(('description',
                                      seoSettings.loginFormDescription))
        elif obj_id == 'register':
            if seoSettings.registerFormDescription:
                self.metatags.append(('description',
                                      seoSettings.registerFormDescription))
        elif adapted:
            found = False
            for i, v in enumerate(self.metatags):
                if v[0] == 'description':
                    found = True
                    self.metatags[i] = (v[0], escape(adapted.description))
            if not found and adapted.description:
                self.metatags.append(('description',
                                      escape(adapted.description)))

        portal_types = getToolByName(self.context, 'portal_types')
        fti = portal_types.getTypeInfo(self.context.portal_type)
        if fti.getProperty('twitter_card', False) and \
                seoSettings.exposeTwitterCard:
            properties = self.context.restrictedTraverse(
                '@@twitter-card-%s' % (fti.getProperty('twitter_card')))()
            self.metatags.extend(properties)

        self.og_metatags = []
        if fti.getProperty('open_graph_type', False) and \
                seoSettings.exposeOpenGraph:
            properties = self.context.restrictedTraverse(
                '@@open-graph-type-%s' % (fti.getProperty('open_graph_type')))()
            self.og_metatags.extend(properties)

        self.itemprops = []
        if seoSettings.exposePublicationDate and \
                self.context.EffectiveDate() != 'None':
            self.itemprops.append(('datePublished',
                                   self.context.effective_date.ISO8601()))


class RobotsViewlet(DublinCoreViewlet):
    index = ViewPageTemplateFile('templates/robots.pt')

    def update(self):
        values = []
        published = getattr(self.request, 'PUBLISHED', None)
        published = getattr(published, 'context', published)
        if IContentish.providedBy(published):
            obj = aq_base(self.context)
            for x in ['seo_noindex', 'seo_nofollow', 'seo_nosnippet',
                      'seo_noarchive']:
                if getattr(obj, x, False):
                    values.append(x.replace('seo_', ''))
        else:
            registry = getUtility(IRegistry)
            seoSettings = registry.forInterface(ISeoSettings)
            obj_id = getattr(published, 'id', '')
            if not obj_id:
                obj_id = self.request.steps[-1].replace('@', '')
            if obj_id == 'contact-info':
                if not seoSettings.indexContactInfo:
                    values.append('noindex')
            elif obj_id in ['login', 'login_form', 'require_login', ]:
                if not seoSettings.indexLoginForm:
                    values.append('noindex')
            elif obj_id == 'register':
                if not seoSettings.indexRegisterForm:
                    values.append('noindex')
            elif obj_id == 'sitemap' or \
                    obj_id == 'accessibility-info' or \
                    obj_id == 'search' or \
                    obj_id == 'mail_password_form':
                values.append('noindex')

        self.content = ', '.join(values)


class CanonicalViewlet(ViewletBase):

    @memoize
    def render(self):
        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        canonical_url = context_state.canonical_object_url()
        obj = aq_base(self.context)
        seo_canonical = getattr(obj, 'seo_canonical', False)
        if seo_canonical:
            canonical_url = seo_canonical.to_object.absolute_url()

        return u'    <link rel="canonical" href="%s" />' % canonical_url


class MultiLanguageViewlet(ViewletBase):

    _template = ViewPageTemplateFile('templates/multilanguage.pt')

    def update(self):
        super(MultiLanguageViewlet, self).update()

        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        canonical_url = context_state.canonical_object_url()
        obj = aq_base(self.context)
        language_links = getattr(obj, 'language_links', False)
        self.links = []
        if language_links:
            for x in language_links:
                self.links.append((x.to_object.language,
                                   x.to_object.absolute_url()))

    @memoize
    def render(self):
        return xhtml_compress(self._template())


class SeoAuthorViewlet(AuthorViewlet):

    _template = ViewPageTemplateFile('templates/author.pt')

    def update(self):
        super(SeoAuthorViewlet, self).update()
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getMemberById(self.context.Creator())
        if member and member.getProperty('google_author', False):
            self.author_url = member.getProperty('google_author')
        else:
            self.author_url = '%s/author/%s' % (self.navigation_root_url,
                                                self.context.Creator())

        registry = getUtility(IRegistry)
        seoSettings = registry.forInterface(ISeoSettings)
        if seoSettings.googlePlusPublisherPage:
            self.publisher_url = seoSettings.googlePlusPublisherPage
        else:
            self.publisher_url = self.navigation_root_url


class FaviconViewlet(ViewletBase):

    _template = ViewPageTemplateFile('templates/favicon.pt')

    def __init__(self, context, request, view, manager=None):
        super(FaviconViewlet, self).__init__(context, request, view, manager)
        registry = getUtility(IRegistry)
        self.seoSettings = registry.forInterface(ISeoSettings)

    def render(self):
        return xhtml_compress(self._template())

    def getValueFor(self, field):
        value = getattr(self.seoSettings, field)
        if value:
            expression = Expression(str(value))
            expression_context = getExprContext(self.context)
            return expression(expression_context)
