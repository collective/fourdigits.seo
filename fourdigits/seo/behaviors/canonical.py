"""Behaviour to add SEO Canonical
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


class ICanonical(form.Schema):
    """Add properties
    """

    form.fieldset(
        'seo',
        label=_(u'SEO'),
        fields=('seo_canonical',
                ),
    )

    seo_canonical = RelationChoice(
        title=_(u"Canonical"),
        description=_(u"Add reference to canonical object."),
        source=ObjPathSourceBinder(),
        required=False,
        )


alsoProvides(ICanonical, IFormFieldProvider)


class Canonical(object):
    """SEO Canonical
    """
    implements(ICanonical)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context