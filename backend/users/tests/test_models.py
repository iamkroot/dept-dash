from django.test import TestCase
from ..models import CustomUser


class CustomUserTest(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            email="f20170124@hyderabad.bits-pilani.ac.in", name="Pranjal Gupta",
        )
        CustomUser.objects.create(
            email="rayt@hyderabad.bits-pilani.ac.in", name="Tathagata Ray",
        )

    def test_user_short_id(self):
        user_a = CustomUser.objects.get(name="Pranjal Gupta")
        user_b = CustomUser.objects.get(name="Tathagata Ray")
        self.assertEqual(user_a.short_id, "f20170124")
        self.assertEqual(user_b.short_id, "rayt")
