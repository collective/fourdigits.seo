from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from z3c.form import form
from zope import schema
from zope.interface import Interface
from plone.z3cform.fieldsets.group import Group
from z3c.form.field import Fields
from fourdigits.seo import MessageFactory as _


class ISeoMetadataSettings(Interface):

    includeSiteNameInTitle = schema.Bool(
        title=u"Include site name in title",
        required=False,
        description=u"Include the site name in the title tag")

    siteNameSeparator = schema.TextLine(
        title=u"Site name separator",
        required=False,
        description=u"Separator used to separate the object title and the site name in the title tag")

    exposePublicationDate = schema.Bool(
        title=u"Expose Publication Date",
        required=False,
        description=u"Expose publication date in the head")

    loginFormTitle = schema.TextLine(
        title=u"Login Form Title",
        required=False,
        max_length=70,
        description=u"Title for the login form")

    loginFormDescription = schema.TextLine(
        title=u"Login Form Description",
        required=False,
        max_length=155,
        description=u"Description for the homepage")

    registerFormTitle = schema.TextLine(
        title=u"Register Form Title",
        required=False,
        max_length=70,
        description=u"Title for the registration form")

    registerFormDescription = schema.TextLine(
        title=u"Register Form Description",
        required=False,
        max_length=155,
        description=u"Description for the registration form")

    contactInfoTitle = schema.TextLine(
        title=u"Contact Info Title",
        required=False,
        max_length=70,
        description=u"Title for the contact info page")

    contactInfoDescription = schema.TextLine(
        title=u"Contact Info Description",
        required=False,
        max_length=155,
        description=u"Description for the contact info page")


class ISeoIndexingSettings(Interface):

    indexLoginForm = schema.Bool(
        title=u"Index Login Form",
        required=False,
        description=u"Whether or not to index the login form")

    indexRegisterForm = schema.Bool(
        title=u"Index Register Form",
        required=False,
        description=u"Whether or not to index the register form")

    indexContactInfo = schema.Bool(
        title=u"Index Contact Info",
        required=False,
        description=u"Whether or not to index the contact info page")


class ISeoSocialSettings(Interface):

    googlePlusPublisherPage = schema.TextLine(
        title=u"Google+ Publisher Page",
        required=False,
        description=u"Fill in your google publisher page, ie. https://plus.google.com/mybrand/")

    exposeTwitterCard = schema.Bool(
        title=u"Expose Twitter Card",
        required=False,
        description=u"Expose Twitter Card using metatags in the head of the document")

    twitterSiteAccount = schema.TextLine(
        title=u"Twitter Site Account",
        required=False,
        description=u"Fill in your twitter site account, ie. @mybrand")

    exposeOpenGraph = schema.Bool(
        title=u"Expose Open Graph",
        required=False,
        description=u"Expose Open Graph using metatags in the head of the document")

    openGraphFallbackImage = schema.TextLine(
        title=u"Open Graph fallback image",
        required=False,
        description=u"Fill in your Open Graph fallback image url (can contain expressions), this is used when the content object doesn't have a leadimage, ie. string:${portal_url}/open-graph-fallback.png")

    exposeAuthorOpenGraph = schema.Bool(
        title=u"Expose Open Graph Author",
        required=False,
        description=u"Expose Open Graph og:article:author information")


class ISeoIconsSettings(Interface):

    favicon = schema.TextLine(
        title=u"Favicon url",
        required=False,
        description=u"Fill in your favicon url (can contain expressions), ie. string:${portal_url}/favicon.ico")

    touchIconIphone = schema.TextLine(
        title=u"Touch icon iPhone url",
        required=False,
        description=u"Fill in your touch icon url (can contain expressions), should be 60x60 pixels, ie. string:${portal_url}/apple-touch-icon.png")

    touchIconIphoneRetina = schema.TextLine(
        title=u"Touch icon iPhone Retina url",
        required=False,
        description=u"Fill in your touch icon url (can contain expressions), should be 120x120 pixels, ie. string:${portal_url}/apple-touch-icon-120x120.png")

    touchIconIpad = schema.TextLine(
        title=u"Touch icon iPad url",
        required=False,
        description=u"Fill in your touch icon url (can contain expressions), should be 76x76 pixels, ie. string:${portal_url}/apple-touch-icon-76x76.png")

    touchIconIpadRetina = schema.TextLine(
        title=u"Touch icon iPad Retina url",
        required=False,
        description=u"Fill in your touch icon url (can contain expressions), should be 152x152 pixels, ie. string:${portal_url}/apple-touch-icon-152x152.png")


class ISeoSettings(ISeoMetadataSettings, ISeoIndexingSettings,
                   ISeoSocialSettings, ISeoIconsSettings):
    """Seo Settings"""


class SeoSocialSettingsForm(Group):
    label = _(u"Social")
    fields = Fields(ISeoSocialSettings)


class SeoIconsSettingsForm(Group):
    label = _(u"Icons")
    fields = Fields(ISeoIconsSettings)


class SeoIndexingSettingsForm(Group):
    label = _(u"Indexing")
    fields = Fields(ISeoIndexingSettings)


class SeoControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISeoSettings
    groups = (SeoSocialSettingsForm, SeoIconsSettingsForm,
              SeoIndexingSettingsForm)


SeoControlPanelView = layout.wrap_form(SeoControlPanelForm,
                                       ControlPanelFormWrapper)
SeoControlPanelView.label = u"SEO settings"
