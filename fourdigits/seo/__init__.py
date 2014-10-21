from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('fourdigits.seo')


import membership
from Products.PlonePAS.tools.membership import MembershipTool
# monkey membership
# https://github.com/plone/Products.PlonePAS/blob/4.2/Products/PlonePAS/tools/membership.py#L346
MembershipTool._orig_getMemberInfo = MembershipTool.getMemberInfo
MembershipTool.getMemberInfo = membership.myGetMemberInfo
