from users.tests.test_views import BaseTestCase
from rest_framework import status


class PublicationTest(BaseTestCase):
    fixtures = ["fixtures.json"]

    def test_hod_can_see_all_publications(self):
        resp = self.hod_client.get(f"/api/publications/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 2)
        self.assertEqual(data[2]["id"], 3)
        self.assertEqual(data[3]["id"], 4)

    def test_hod_can_see_specific_publications(self):
        resp = self.hod_client.get(f"/api/publications/4/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 4)

        resp = self.hod_client.get(f"/api/publications/2/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 2)

    def test_hod_can_update_his_publications(self):
        resp = self.hod_client.patch(
            f"/api/publications/2/",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_hod_cannot_update_others_publications(self):
        resp = self.hod_client.patch(
            f"/api/publications/4/",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_see_only_his_publications(self):
        resp = self.faculty_1_client.get(f"/api/publications/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 4)

    def test_faculty_can_see_his_specific_publications(self):
        resp = self.faculty_1_client.get(f"/api/publications/1/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 1)

    def test_faculty_cannot_see_others_publications(self):
        resp = self.faculty_1_client.get(f"/api/publications/3/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_update_his_publications(self):
        resp = self.faculty_1_client.patch(
            f"/api/publications/1/",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_faculty_cannot_update_other_publications(self):
        resp = self.faculty_1_client.patch(
            f"/api/publications/3/",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class ProjectTest(BaseTestCase):
    fixtures = ["fixtures.json"]

    def test_hod_can_see_all_projects(self):
        resp = self.hod_client.get(f"/api/projects/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 2)
        self.assertEqual(data[2]["id"], 3)
        self.assertEqual(data[3]["id"], 4)

    def test_hod_can_see_specific_project(self):
        resp = self.hod_client.get(f"/api/projects/2/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 2)

        resp = self.hod_client.get(f"/api/projects/3/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 3)

        resp = self.hod_client.get(f"/api/projects/4/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 4)

    def test_hod_can_update_his_project(self):
        resp = self.hod_client.patch(
            f"/api/projects/2",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.hod_client.patch(
            f"/api/projects/4",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_hod_cannot_update_others_projects(self):
        resp = self.hod_client.patch(
            f"/api/projects/1",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_see_his_projects(self):
        resp = self.faculty_1_client.get(f"/api/projects/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[1]["id"], 2)

    def test_faculty_can_see_specific_projects(self):
        resp = self.faculty_1_client.get(f"/api/projects/1/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 1)

        resp = self.faculty_1_client.get(f"/api/projects/2/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], 2)

    def test_faculty_cannot_see_others_projects(self):
        resp = self.faculty_1_client.get(f"/api/projects/3/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_update_his_project(self):
        resp = self.faculty_1_client.patch(
            f"/api/projects/1/",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.faculty_1_client.patch(
            f"/api/projects/2/",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_faculty_cannot_update_other_projects(self):
        resp = self.faculty_1_client.patch(
            f"/api/projects/3/",
            {"status": "COM"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
