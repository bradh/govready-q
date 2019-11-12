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

    def test_itsystem_creation(self):
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
        self.assertInNodeText("You do not have access to any Hosts for this IT System.", "div.container p")

        self.click_element("a#new-itsystem-host")
        # next steps: create the Host, see what else is needed

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

