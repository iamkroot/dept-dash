from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Faculty, ResearchScholar
from auth.views import get_token_for_user


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.faculty_user = Faculty.objects.get(psrn=3)
        faculty_user_token = get_token_for_user(cls.faculty_user)
        cls.faculty_client = APIClient()
        cls.faculty_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {faculty_user_token}"
        )

        cls.hod_user = Faculty.objects.get(psrn=2)
        hod_user_token = get_token_for_user(cls.hod_user)
        cls.hod_client = APIClient()
        cls.hod_client.credentials(HTTP_AUTHORIZATION=f"Bearer {hod_user_token}")

        cls.scholar_user = ResearchScholar.objects.get(id_num="2017A7PS0703H")
        scholar_user_token = get_token_for_user(cls.scholar_user)
        cls.scholar_client = APIClient()
        cls.scholar_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {scholar_user_token}"
        )


class FacultyViewTest(BaseTestCase):
    fixtures = ["fixtures.json"]

    def test_faculty_can_see_list(self):
        resp = self.faculty_client.get(reverse("faculty-list"))
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)
        self.assertSetEqual(
            set(data[0].keys()), {'email', 'alt_email', 'contact_num', 'name', 'psrn'}
        )

    def test_faculty_can_see_own_detail(self):
        resp = self.faculty_client.get(reverse("faculty-detail", kwargs={"pk": 3}))
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertSetEqual(
            set(data.keys()), {'email', 'alt_email', 'contact_num', 'name', 'psrn'}
        )

    def test_faculty_cannot_see_others_detail(self):
        resp = self.faculty_client.get(reverse("faculty-detail", kwargs={"pk": 2}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_update_self(self):
        resp = self.faculty_client.patch(
            reverse("faculty-detail", kwargs={"pk": 3}),
            {"alt_email": "abc@example.com"},
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_hod_can_see_list(self):
        resp = self.hod_client.get(reverse("faculty-list"))
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)
        self.assertSetEqual(
            set(data[0].keys()), {'email', 'alt_email', 'contact_num', 'name', 'psrn'}
        )

    def test_hod_can_see_any_detail(self):
        resp = self.hod_client.get(reverse("faculty-detail", kwargs={"pk": 3}))
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertSetEqual(
            set(data.keys()), {'email', 'alt_email', 'contact_num', 'name', 'psrn'}
        )

    def test_hod_cannot_update_other(self):
        resp = self.hod_client.patch(
            reverse("faculty-detail", kwargs={"pk": 3}),
            {"alt_email": "abc@example.com"},
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_scholar_cannot_see_list(self):
        resp = self.scholar_client.get(reverse("faculty-list"))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_scholar_cannot_see_detail(self):
        resp = self.scholar_client.get(reverse("faculty-detail", kwargs={"pk": 3}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
