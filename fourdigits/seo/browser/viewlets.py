from cgi import escape
from plone.app.layout.viewlets.common import TitleViewlet
from plone.app.layout.links.viewlets import render_cachekey
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


class SeoTitleViewlet(TitleViewlet):

    @property
    @memoize
    def page_title(self):
        '''
        Override the pagetitle when seo title is specified
        '''
        adapted = ISeoAdapter(self.context, None)
        if adapted:
            return escape(adapted.title)
        else:
            return super(SeoTitleViewlet, self).page_title


class SeoDublinCoreViewlet(DublinCoreViewlet):
    def update(self):
        super(SeoDublinCoreViewlet, self).update()

        adapted = ISeoAdapter(self.context, None)
        if adapted:
            found = False
            for i, v in enumerate(self.metatags):
                if v[0] == 'description':
                    found = True
                    self.metatags[i] = (v[0], escape(adapted.description))
            if not found and adapted.description:
                self.metatags.append(('description',
                                      escape(adapted.description)))

        registry = getUtility(IRegistry)
        seoSettings = registry.forInterface(ISeoSettings)

        portal_types = getToolByName(self.context, 'portal_types')
        fti = portal_types.getTypeInfo(self.context.portal_type)
        if fti.getProperty('twitter_card', False) and \
            seoSettings.exposeTwitterCard:
            properties = self.context.restrictedTraverse(
                '@@twitter-card-%s' % (fti.getProperty('twitter_card')))()
            self.metatags.extend(properties)

        if fti.getProperty('open_graph_type', False) and \
            seoSettings.exposeOpenGraph:
            properties = self.context.restrictedTraverse(
                '@@open-graph-type-%s' % \
                    (fti.getProperty('open_graph_type')))()
            self.metatags.extend(properties)


class RobotsViewlet(DublinCoreViewlet):
    index = ViewPageTemplateFile('templates/robots.pt')

    def update(self):
        values = []
        published = self.request['PUBLISHED']
        if IContentish.providedBy(published):
            obj = aq_base(self.context)
            for x in ['seo_noindex', 'seo_nofollow', 'seo_nosnippet',
                      'seo_noarchive']:
                if getattr(obj, x, False):
                    values.append(x.replace('seo_', ''))
        else:
            registry = getUtility(IRegistry)
            seoSettings = registry.forInterface(ISeoSettings)
            if getattr(published, 'id', '') == 'contact-info':
                if not seoSettings.indexingContactInfo:
                    values.append('noindex')
            elif getattr(published, 'id', '') in ['login', 'login_form']:
                if not seoSettings.indexingLoginForm:
                    values.append('noindex')
            elif self.request.steps[-1] in 'register':
                if not seoSettings.indexingRegisterForm:
                    values.append('noindex')
        
        self.content = ', '.join(values)


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
