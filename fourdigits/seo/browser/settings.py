from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from z3c.form import form
from zope import schema
from zope.interface import Interface


class ISeoSettings(Interface):
    """ Define settings data structure """

    googlePlusPublisherPage = schema.TextLine(title=u"Google+ Publisher Page",
            required=False,
            description=u"Fill in your google publisher page, ie. https://plus.google.com/mybrand/")

    twitterSiteAccount = schema.TextLine(title=u"Twitter Site Account",
            required=False,
            description=u"Fill in your twitter site account, ie. @mybrand")

    favicon = schema.TextLine(title=u"Favicon url",
            required=False,
            description=u"Fill in your favicon url (can contain expressions), ie. string:${portal_url}/favicon.ico")

    touch_icon_iphone = schema.TextLine(title=u"Touch icon iPhone url",
            required=False,
            description=u"Fill in your touch icon url (can contain expressions), should be 60x60 pixels, ie. string:${portal_url}/apple-touch-icon.png")

    touch_icon_iphone_retina = schema.TextLine(title=u"Touch icon iPhone Retina url",
            required=False,
            description=u"Fill in your touch icon url (can contain expressions), should be 120x120 pixels, ie. string:${portal_url}/apple-touch-icon-120x120.png")

    touch_icon_ipad = schema.TextLine(title=u"Touch icon iPad url",
            required=False,
            description=u"Fill in your touch icon url (can contain expressions), should be 76x76 pixels, ie. string:${portal_url}/apple-touch-icon-76x76.png")

    touch_icon_ipad_retina = schema.TextLine(title=u"Touch icon iPad Retina url",
            required=False,
            description=u"Fill in your touch icon url (can contain expressions), should be 152x152 pixels, ie. string:${portal_url}/apple-touch-icon-152x152.png")

    open_graph_fallback_image = schema.TextLine(title=u"Open Graph fallback image",
            required=False,
            description=u"Fill in your Open Graph fallback image url (can contain expressions), this is used when the content object doesn't have a leadimage, ie. string:${portal_url}/open-graph-fallback.png")


class SeoControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISeoSettings


SeoControlPanelView = layout.wrap_form(SeoControlPanelForm, ControlPanelFormWrapper)
SeoControlPanelView.label = u"SEO settings"
