"""Behaviour to add SEO Image
"""
from fourdigits.seo import MessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements


class IImage(form.Schema):
    """Add properties
    """

    form.fieldset(
        'seo',
        label=_(u'SEO'),
        fields=('seo_image',
                ),
    )

    seo_image = RelationChoice(
        title=_(u"Image"),
        description=_(u"Add image when social sharing this page."),
        source=ObjPathSourceBinder(),
        required=False,
        )


alsoProvides(IImage, IFormFieldProvider)


class Image(object):
    """SEO Image
    """
    implements(IImage)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
