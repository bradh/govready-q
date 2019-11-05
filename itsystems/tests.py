from django.test import TestCase
from .models import System

class SystemModelTest(TestCase):
    def testAbsoluteUrl(self):
        obj = System.objects.create(
            id=42,
        )

        self.assertEqual('/itsystems/42/', obj.get_absolute_url())

    # not clear if the behaviour of str(system_object) is specced or not, but let's test it nonetheless
    def testStrValue(self):
        name = "Some System"
        obj = System.objects.create(
            name=name,
        )

        self.assertEqual(name, str(obj))
