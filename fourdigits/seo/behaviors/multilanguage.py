"""Behaviour to add SEO Multi Language
"""
from fourdigits.seo import MessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements


class IMultiLanguage(form.Schema):
    """Add properties
    """

    form.fieldset(
        'seo',
        label=_(u'SEO'),
        fields=('language_links',
                ),
    )

    language_links = RelationList(
        title=_(u"Language Links"),
        description=_(u"Add reference to other languages of the same content."),
        value_type=RelationChoice(
            title=_(u"Language Links"),
            source=ObjPathSourceBinder(),
            required=False,
        ),
        required=False,
    )


alsoProvides(IMultiLanguage, IFormFieldProvider)


class MultiLanguage(object):
    """SEO Multi Language
    """
    implements(IMultiLanguage)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context