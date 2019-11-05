from django.test import TestCase
from .models import System


class SystemModelTest(TestCase):
    def testAbsoluteUrl(self):
        obj = System.objects.create(
            id=42,
        )

        self.assertEqual('/itsystems/42/', obj.get_absolute_url())

    def testModelStructure(self):
        test_string = "some string"
        obj = System.objects.create(
            name=test_string,
            sdlc_stage=test_string,
        )

        self.assertIsInstance(obj, System)

    # not clear if the behaviour of str(system_object) is specced or not, but let's test it nonetheless
    def testStrValue(self):
        name = "Some System"
        obj = System.objects.create(
            name=name,
        )

        self.assertEqual(name, str(obj))
