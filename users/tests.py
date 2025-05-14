from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User

class UserModelTest(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123!"
        }

    def test_create_user(self):
        user = User.objects.create_user(
            email=self.user_data["email"],
            password=self.user_data["password"],
            username=self.user_data["username"]
        )
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertEqual(str(user), self.user_data["email"])

class UserAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user1@example.com",
            password="Pass1234!",
            username="user1"
        )
        self.group_teacher, _ = Group.objects.get_or_create(name="teachers")
        self.teacher_user = User.objects.create_user(
            email="teacher@example.com",
            password="Pass1234!",
            username="teacher"
        )
        self.teacher_user.groups.add(self.group_teacher)
        self.superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPass123!",
            username="admin"
        )

    def test_register_user(self):
        url = reverse('users:register')
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "NewPass123!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_list_users(self):
        url = reverse('users:user_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_login_token(self):
        url = reverse('users:login')
        data = {
            "email": self.user.email,
            "password": "Pass1234!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_refresh(self):
        token_response = self.client.post(reverse('users:login'), {
            "email": self.user.email,
            "password": "Pass1234!"
        })
        refresh_token = token_response.data['refresh']
        url = reverse('users:token_refresh')
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_is_teacher_permission(self):
        self.client.force_authenticate(user=self.teacher_user)
        permission = self._check_permission_is_teacher()
        self.assertTrue(permission)

        self.client.force_authenticate(user=self.superuser)
        permission = self._check_permission_is_teacher()
        self.assertTrue(permission)

        self.client.force_authenticate(user=self.user)
        permission = self._check_permission_is_teacher()
        self.assertFalse(permission)

    def _check_permission_is_teacher(self):
        from users.permissions import IsTeacher
        permission = IsTeacher()
        request = self._build_request()
        request.user = self.client.handler._force_user
        request._auth = None
        return permission.has_permission(request, view=None)

    def _build_request(self):
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        return factory.get('/')
