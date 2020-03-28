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
        for faculty in Faculty.objects.all():
            token = get_token_for_user(faculty)
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            if faculty.is_hod:
                cls.hod = faculty
                cls.hod_client = client
            else:
                setattr(cls, f"faculty_{faculty.psrn}", faculty)
                setattr(cls, f"faculty_{faculty.psrn}_client", client)

        cls.scholar_user = ResearchScholar.objects.get(id_num="2017A7PS0703H")
        scholar_user_token = get_token_for_user(cls.scholar_user)
        cls.scholar_client = APIClient()
        cls.scholar_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {scholar_user_token}"
        )


class FacultyViewTest(BaseTestCase):
    fixtures = ["fixtures.json"]

    def test_faculty_can_see_list(self):
        resp = self.faculty_3_client.get(reverse("faculty-list"))
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)
        self.assertSetEqual(
            set(data[0].keys()), {'email', 'alt_email', 'contact_num', 'name', 'psrn'}
        )

    def test_faculty_can_see_own_detail(self):
        resp = self.faculty_3_client.get(reverse("faculty-detail", kwargs={"pk": 3}))
        data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertSetEqual(
            set(data.keys()), {'email', 'alt_email', 'contact_num', 'name', 'psrn'}
        )

    def test_faculty_cannot_see_others_detail(self):
        resp = self.faculty_3_client.get(reverse("faculty-detail", kwargs={"pk": 2}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_update_self(self):
        resp = self.faculty_3_client.patch(
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


class FacultyNestedViewTest(BaseTestCase):
    fixtures = ["fixtures.json"]

    def test_faculty_can_see_own_research_list(self):
        # faculty 1
        resp = self.faculty_1_client.get(f"/api/faculties/1/projects/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        # assert that own projects are included
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 2)

        # TODO: Test publications similarly

        # faculty 3
        resp = self.faculty_3_client.get(f"/api/faculties/3/projects/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 2)
        self.assertEqual(data[1]["id"], 3)

    def test_faculty_cannot_see_others_research(self):
        # TODO: Make this pass
        resp = self.faculty_1_client.get(f"/api/faculties/3/projects/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        resp = self.faculty_1_client.get(f"/api/faculties/3/publications/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_hod_can_see_own_research(self):
        resp = self.hod_client.get(f"/api/faculties/2/projects/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 2)

    def test_hod_can_see_others_research(self):
        resp = self.hod_client.get(f"/api/faculties/3/projects/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 2)
        self.assertEqual(data[1]["id"], 3)
