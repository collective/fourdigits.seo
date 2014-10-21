from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.interface import implements
from fourdigits.seo import MessageFactory as _
from zope.schema.vocabulary import SimpleVocabulary


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    linkedin_author = schema.TextLine(
        title=_(u'label_linkedin_author', default=u'Linkedin author'),
        description=_(u'help_linkedin_author',
                      default=u"Fill in your linkedin author page, ie. http://nl.linkedin.com/in/username"),
        required=False,
    )

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
                      default=u"Fill in your facebook id, or the url to your profile page"),
        required=False,
    )

    first_name = schema.TextLine(
        title=_(u'label_first_name', default=u'First name'),
        description=_(u'help_first_name',
                      default=u"Fill in your first name"),
        required=False,
    )

    last_name = schema.TextLine(
        title=_(u'label_last_name', default=u'Last name'),
        description=_(u'help_last_name',
                      default=u"Fill in your last name"),
        required=False,
    )

    gender = schema.Choice(
        title=_(u'label_gender', default=u'Gender'),
        description=_(u'help_gender',
                      default=u"Fill in your gender"),
        source=SimpleVocabulary([
            SimpleVocabulary.createTerm('male', 'male', _('Male')),
            SimpleVocabulary.createTerm('female', 'female', _('Female'))]),
        required=False,
        )


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    def get_linkedin_author(self):
        return self.context.getProperty('linkedin_author', '')
    def set_linkedin_author(self, value):
        return self.context.setMemberProperties({'linkedin_author': value})
    linkedin_author = property(get_linkedin_author, set_linkedin_author)

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

    def get_first_name(self):
        return self.context.getProperty('first_name', '')
    def set_first_name(self, value):
        return self.context.setMemberProperties({'first_name': value})
    first_name = property(get_first_name, set_first_name)

    def get_last_name(self):
        return self.context.getProperty('last_name', '')
    def set_last_name(self, value):
        return self.context.setMemberProperties({'last_name': value})
    last_name = property(get_last_name, set_last_name)

    def get_gender(self):
        return self.context.getProperty('gender', '')
    def set_gender(self, value):
        return self.context.setMemberProperties({'gender': value})
    gender = property(get_gender, set_gender)
