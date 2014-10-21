from Products.PlonePAS.tools.membership import MembershipTool


def myGetMemberInfo(self, memberId=None):
    """
    Return 'harmless' Memberinfo of any member, such as Full name,
    Location, etc
    #https://github.com/plone/Products.PlonePAS/blob/4.2/Products/PlonePAS/tools/membership.py#L346
    """
    memberinfo = MembershipTool._orig_getMemberInfo(self, memberId)

    if memberinfo is None:
        return None

    if not memberId:
        member = self.getAuthenticatedMember()
    else:
        member = self.getMemberById(memberId)

    if member is None:
        return None

    memberinfo = {
        'fullname': member.getProperty('fullname'),
        'description': member.getProperty('description'),
        'location': member.getProperty('location'),
        'language': member.getProperty('language'),
        'home_page': member.getProperty('home_page'),
        'username': member.getUserName(),
        'has_email': bool(member.getProperty('email')),
        'linkedin_author': unicode(member.getProperty('linkedin_author', ''), 'utf-8'),
        'google_author': unicode(member.getProperty('google_author', ''), 'utf-8'),
        'twitter_author': unicode(member.getProperty('twitter_author', ''), 'utf-8'),
        'facebook_id': unicode(member.getProperty('facebook_id', ''), 'utf-8'),
        'first_name': unicode(member.getProperty('first_name', ''), 'utf-8'),
        'last_name': unicode(member.getProperty('last_name', ''), 'utf-8'),
        'gender': unicode(member.getProperty('gender', ''), 'utf-8'),
    }

    return memberinfo
