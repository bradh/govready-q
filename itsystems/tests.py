from django.test import TestCase
from .models import System, Host, AgentService, Agent, Vendor, Component

from siteapp.tests import SeleniumTest, OrganizationSiteFunctionalTests

class WebTest(OrganizationSiteFunctionalTests):
    def _output_source(self, name):
        with open("local/{}.debug.html".format(name), 'w') as file:
            file.write(self.browser.page_source)
    def test_homepage(self):
        self.browser.get(self.url("/"))
        self.assertRegex(self.browser.title, "Welcome to Compliance Automation")

    def testSystemAndHostCreation(self):
        self._login()

        # load the module entry point's URL
        self.browser.get(self.url("/itsystems"))
        # we assume no IT Systems have been created yet - verify this
        self.assertEqual(0, System.objects.count())
        self.assertInNodeText("You do not have access to any IT Systems.", "div.container p")

        # create a new system: first, load that page
        self.click_element('a#new-itsystem')

        # and fill in some test data
        self.fill_field("#id_name", "Test System")
        self.fill_field("#id_sdlc_stage", "Deployed")
        self.click_element("form button#create-itsystems-button[type=submit]")
        # presumably, we've now created an IT System
        self.assertEqual(1, System.objects.count())

        # and now, we'll need to create some Hosts
        self.assertInNodeText("Add a Host", "a#new-itsystem-host")
        self.assertEqual(0, Host.objects.count())
        self.assertInNodeText("You do not have access to any Hosts for this IT System.", "div.container p")

        self.click_element("a#new-itsystem-host")

        self.fill_field('#id_name', 'Test Host')
        self.fill_field('#id_host_type', 'Webserver')
        self.fill_field('#id_os', 'Windows 10')
        self.select_option_by_visible_text('#id_system', "Test System")
        self.click_element("form button#create-hostsystems-button[type=submit]")

        self.assertEqual(1, Host.objects.count())
        self.assertNotInNodeText('Server Error', 'body')
        # might be worth adding some more assertions here


    def testVendorAndComponentCreation(self):
        self._login()

        self.assertEqual(0, Component.objects.count())
        self.assertEqual(0, Vendor.objects.count())

        # navigate to the Components list page
        # do this starting from the main itsystems page, to verify that it's actually UI-accessible
        self.browser.get(self.url("/itsystems"))
        # do *= for contains, so that we can make it absolute or add a trailing slash without breaking the test
        self.click_element('a[href*="components/list"]') 
        
        self.click_element('a#new-vendor')

        self.fill_field('#id_name', 'Test Vendor')
        self.click_element("form button#create-itsystems-button[type=submit]")
        self.assertEqual(1, Vendor.objects.count())
        self.assertNotInNodeText('Server Error', 'body')
        
        self.click_element('a#new-component')
        self.fill_field('#id_name', 'Test Component')
        self.fill_field('#id_version', '1.0.0')
        self.select_option_by_visible_text('#id_vendor', "Test Vendor")
        self.click_element("form button#create-component-button[type=submit]")
        self.assertEqual(1, Component.objects.count())
        self.assertEqual("Test Vendor", Component.objects.get().vendor.name)
        self.assertNotInNodeText('Server Error', 'body')


    def testComponentRequiresVendor(self):
        self._login()

        self.browser.get(self.url("/itsystems/components/new"))

        component_count = Component.objects.count()

        # create a Component, with no linked Vendor. This is expected to fail.
        self.fill_field('#id_name', 'Test Component')
        self.fill_field('#id_version', '1.0.0')
        self.click_element("form button#create-component-button[type=submit]")

        # count of Components should be the same - nothing should have been created
        self.assertEqual(component_count, Component.objects.count())

        # the HTML response can be anything, as long as the count didn't change

        self._output_source('it-fail-component')
    
    # this is a somewhat weak test - would be better to test Host and AgentService separately
    def testAgentRequiresHostPlusAgentService(self):
        self._login()
        
        self.browser.get(self.url("/itsystems/agents/new"))

        agent_count = Agent.objects.count()

        self.fill_field('#id_agent_id', 'Test Agent')
        self.click_element("form button#create-hostsystems-button[type=submit]")

        self.assertEqual(agent_count, Agent.objects.count())

        self._output_source('it-fail-agent')


class ModelTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.unique_counter = 0

    def getString(self):
        return "some string"

    def getUniqueString(self):
        id = self.unique_counter
        self.unique_counter += 1
        return self.getString() + "_" + str(id)

    def makeSystem(self):
        return System.objects.create(
            name=self.getUniqueString(),
            sdlc_stage=self.getString(),
        )

    def makeHost(self):
        return Host.objects.create(
            name=self.getUniqueString(),
            host_type=self.getString(),
            os=self.getString(),
            system=self.makeSystem(),
        )

    def makeAgentService(self):
        return AgentService.objects.create(
            name=self.getUniqueString(),
            api_user=self.getString(),
            api_pw=self.getString(),
        )

    def makeAgent(self):
        return Agent.objects.create(
            agent_id=self.getString(), # should this be unique? (need to check specs)
            agent_service=self.makeAgentService(),
            host=self.makeHost(),
        )

    def makeVendor(self):
        return Vendor.objects.create(
            name=self.getUniqueString(),
        )

    def makeComponent(self):
        return Component.objects.create(
            name=self.getUniqueString(),
            vendor=self.makeVendor(),
            version=self.getString(),
        )


class SystemModelTest(ModelTest):
    def testAbsoluteUrl(self):
        obj = System.objects.create(
            id=42,
        )

        self.assertEqual('/itsystems/42/', obj.get_absolute_url())

    def testModelStructure(self):
        obj = self.makeSystem()
        self.assertIsInstance(obj, System)

    # not clear if the behaviour of str(system_object) is specced or not, but let's test it nonetheless
    def testStrValue(self):
        name = self.getUniqueString()
        obj = System.objects.create(
            name=name,
        )

        self.assertEqual(name, str(obj))

class HostModelTest(ModelTest):
    def testModelStructure(self):
        obj = self.makeHost()
        self.assertIsInstance(obj, Host)

class AgentServiceModelTest(ModelTest):
    def testModelStructure(self):
        obj = self.makeAgentService()
        self.assertIsInstance(obj, AgentService)

class AgentModelTest(ModelTest):
    def testModelStructure(self):
        obj = self.makeAgent()
        self.assertIsInstance(obj, Agent)

class VendorModelTest(ModelTest):
    def testModelStructure(self):
        obj = self.makeVendor()
        self.assertIsInstance(obj, Vendor)

class ComponentModelTest(ModelTest):
    def testModelStructure(self):
        obj = self.makeComponent()
        self.assertIsInstance(obj, Component)

