from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
import logging
PROFILE_ID = 'profile-fourdigits.seo:default'


def upgradestep_0001_to_1001(context, logger=None):
    if logger is None:
        logger = logging.getLogger('fourdigits.seo')

    setup = getToolByName(context, 'portal_setup')

    # add discussion_notification
    setup.runImportStepFromProfile(PROFILE_ID,
                                   'memberdata-properties',
                                   run_dependencies=False,
                                   purge_old=False)

    mtool = getToolByName(context, 'portal_membership')
    members = mtool.listMemberIds()
    for objid in members:
        member = mtool.getMemberById(objid)
        member.setMemberProperties({'linkedin_author': ''})

    logger.info("Upgraded fourdigits.seo to 1001.")
