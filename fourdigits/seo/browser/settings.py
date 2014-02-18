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


class SeoControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISeoSettings


SeoControlPanelView = layout.wrap_form(SeoControlPanelForm, ControlPanelFormWrapper)
SeoControlPanelView.label = u"SEO settings"
