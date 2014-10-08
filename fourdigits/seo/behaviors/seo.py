"""Behaviour to add SEO Properties
"""
from fourdigits.seo import MessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form
from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode


class ISeo(form.Schema):
    """Add properties
    """

    form.fieldset(
        'seo',
        label=_(u'SEO'),
        fields=('seo_title',
                'seo_description',
                'seo_noindex',
                'seo_nofollow',
                'seo_noarchive',
                'seo_nosnippet',
                ),
    )

    seo_title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Override the meta title. When empty the default title will be used. Use maximum 50 chararcters."),
        required=False,
        max_length=70,
    )

    seo_description = schema.TextLine(
        title=_(u"Description"),
        description=_(u"Override the meta description. When empty the default description will be used. Use maximum 150 characters."),
        required=False,
        max_length=155,
    )

    seo_noindex = schema.Bool(
        title=_(u"No Index"),
        description=_(u"Tells search engines not to index this page"),
        required=False,
    )

    seo_nofollow = schema.Bool(
        title=_(u"No Follow"),
        description=_(u"Tells search engines not to follow links on this page"),
        required=False,
    )

    seo_noarchive = schema.Bool(
        title=_(u"No Archive"),
        description=_(u"Tells search engines not to store a cached copy of this page"),
        required=False,
    )

    seo_nosnippet = schema.Bool(
        title=_(u"No Snippet"),
        description=_(u"Tells search engines not to show a snippet under your listing"),
        required=False,
    )

alsoProvides(ISeo, IFormFieldProvider)


class Seo(object):
    """SEO Properties
    """
    implements(ISeo)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context


class ISeoAdapter(Interface):
    """SEO Adapter
    """


class SeoAdapter(object):
    """Seo Adapter Class
    """
    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        if getattr(self.context.aq_base, 'seo_title', False):
            return safe_unicode(self.context.seo_title)
        else:
            return safe_unicode(self.context.Title())

    @property
    def description(self):
        if getattr(self.context.aq_base, 'seo_description', False):
            return safe_unicode(self.context.seo_description)
        else:
            return u' '.join(safe_unicode(self.context.Description()).split())
