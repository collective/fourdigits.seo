from cgi import escape
from plone.app.layout.viewlets.common import TitleViewlet
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

        portal_types = getToolByName(self.context, 'portal_types')
        fti = portal_types.getTypeInfo(self.context.portal_type)
        if fti.getProperty('twitter_card', False):
            properties = self.context.restrictedTraverse(
                '@@twitter-card-%s' % (fti.getProperty('twitter_card')))()
            self.metatags.extend(properties)

        if fti.getProperty('open_graph_type', False):
            properties = self.context.restrictedTraverse(
                '@@open-graph-type-%s' % \
                    (fti.getProperty('open_graph_type')))()
            self.metatags.extend(properties)


class RobotsViewlet(DublinCoreViewlet):
    index = ViewPageTemplateFile('templates/robots.pt')

    def update(self):
        values = []
        obj = aq_base(self.context)
        for x in ['seo_noindex', 'seo_nofollow', 'seo_nosnippet',
                  'seo_noarchive']:
            if getattr(obj, x, False):
                values.append(x.replace('seo_', ''))
        
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
