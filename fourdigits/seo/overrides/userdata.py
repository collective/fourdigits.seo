from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.interface import implements
from fourdigits.seo import MessageFactory as _


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    google_author = schema.TextLine(
        title=_(u'label_google_author', default=u'Google author'),
        description=_(u'help_google_author',
            default=u"Fill in your google author page, ie. https://plus.google.com/123456789012345678901/"),
        required=False,
        )

    twitter_author = schema.TextLine(
        title=_(u'label_twitter_author', default=u'Twitter author'),
        description=_(u'help_twitter_author',
            default=u"Fill in your twitter author, ie. @johndoe"),
        required=False,
        )

    facebook_id = schema.TextLine(
        title=_(u'label_facebook_id', default=u'Facebook ID'),
        description=_(u'help_facebook_id',
            default=u"Fill in your facebook id, ie. 1234567890"),
        required=False,
        )


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    def get_google_author(self):
        return self.context.getProperty('google_author', '')
    def set_google_author(self, value):
        return self.context.setMemberProperties({'google_author': value})
    google_author = property(get_google_author, set_google_author)

    def get_twitter_author(self):
        return self.context.getProperty('twitter_author', '')
    def set_twitter_author(self, value):
        return self.context.setMemberProperties({'twitter_author': value})
    twitter_author = property(get_twitter_author, set_twitter_author)

    def get_facebook_id(self):
        return self.context.getProperty('facebook_id', '')
    def set_facebook_id(self, value):
        return self.context.setMemberProperties({'facebook_id': value})
    facebook_id = property(get_facebook_id, set_facebook_id)
