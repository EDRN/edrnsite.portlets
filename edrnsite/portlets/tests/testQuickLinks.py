# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from base import BaseTestCase
from zope.app.component.hooks import setHooks, setSite
from edrnsite.portlets.portlets import quicklinks
from plone.portlets.interfaces import IPortletType, IPortletAssignment, IPortletDataProvider, IPortletManager, IPortletRenderer
from zope.component import getUtility, getMultiAdapter
from Products.GenericSetup.utils import _getDottedName

class TestPortlet(BaseTestCase):
    def afterSetUp(self):
        setHooks()
        setSite(self.portal)
        self.setRoles(('Manager',))
    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name=u'edrnsite.portlets.QuickLinks')
        self.assertEquals(portlet.addview, u'edrnsite.portlets.QuickLinks')
    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name=u'edrnsite.portlets.QuickLinks')
        registeredInterfaces = [_getDottedName(i) for i in portlet.for_]
        registeredInterfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn', 'plone.app.portlets.interfaces.IDashboard'],
            registeredInterfaces)
    def testInterfaces(self):
        portlet = quicklinks.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet))
    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name=u'edrnsite.portlets.QuickLinks')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview()
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], quicklinks.Assignment))
    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = quicklinks.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, quicklinks.Renderer))

class TestRenderer(BaseTestCase):
    def afterSetUp(self):
        setHooks()
        setSite(self.portal)
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or quicklinks.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
    def testAvailable(self):
        # Investigators are now part of sites, so make sure they're no longer in the portlet
        html = self.renderer().render()
        self.failUnless('Investigators' not in html)
        # CA-449 says we need a Specimens button—nope, not any more: Dan wants Specimens to be a globalnav tab.
        self.failIf('Specimens' in html)
        # CA-466 specifies a new order of portlets, adds Standards, removes Calendar
        # Also, we have Collaborative Groups now as the #1 item
        collabGrps = html.index('Collaborative Groups')
        advocates  = html.index('Public, Patients, Advocates')
        funding    = html.index('Funding Opportunities')
        sites      = html.index('Sites')
        committees = html.index('Committees')
        standards  = html.index('Biomarker Informatics Standards')
        dcp        = html.index('Division of Cancer Prevention')
        cbrg       = html.index('Cancer Biomarkers Research Group')
        bookshelf  = html.index('Bookshelf')
        self.failUnless(collabGrps < advocates < funding < sites < committees < standards < dcp < cbrg < bookshelf)
        # CA-642 wants a "New Members" button, but CA-692 says it should be a link to EDRN Secure Site
        self.failIf('New Members' in html)
        self.failUnless('Secure Site' in html)
        # Dan wants a Members List button (CA-789, Christos wants it to be "Member Directory")
        self.failUnless('>Member Directory<' in html)
        # Dan wants the Members List right after the sites button (CA-789, Christos wants it to be "Member Directory")
        membersList = html.index('>Member Directory<')
        self.failUnless(sites < membersList)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite

        
