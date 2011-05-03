# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
Testing base code.
'''

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

# Traditional Products we have to load manually for test cases:
# (none at this time)

@onsetup
def setupEDRNSitePortlets():
    '''Set up additional products required.'''
    fiveconfigure.debug_mode = True
    import edrnsite.portlets
    zcml.load_config('configure.zcml', edrnsite.portlets)
    fiveconfigure.debug_mode = False
    ztc.installPackage('edrnsite.portlets')

setupEDRNSitePortlets()
ptc.setupPloneSite(products=['edrnsite.portlets'])

class BaseTestCase(ptc.PloneTestCase):
    '''Base for tests in this package.'''
    pass
    

class FunctionalBaseTestCase(ptc.FunctionalTestCase):
    '''Base class for functional (doc-)tests.'''
    pass
