from django.test import TestCase
from .models import ControlService

# Create your tests here.

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

    def makeControlService(self):
        return ControlService.objects.create(
            name=self.getUniqueString(),
            api_user=self.getString(),
            api_pw=self.getString(),
        )

class ControlServiceModel(ModelTest):
    def testModelStructure(self):
        obj = self.makeControlService()
        self.assertIsInstance(obj, ControlService)
