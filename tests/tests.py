from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from learning_platform.models import Course, Lesson
from .models import Test
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class TestQuizTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teachpass')
        self.client.force_authenticate(user=self.teacher)
        self.course = Course.objects.create(name="Python", description="desc", owner=self.teacher)
        self.lesson = Lesson.objects.create(name="Intro", description="desc", course=self.course, owner=self.teacher)

    def test_create_test(self):
        url = reverse('tests:test-list')
        data = {
            "lesson": self.lesson.id,
            "question": "2+2?",
            "option_1": "3",
            "option_2": "4",
            "option_3": "5",
            "option_4": "6",
            "correct_option": 2,
            "explanation": "2+2=4"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_answer(self):
        test = Test.objects.create(
            lesson=self.lesson,
            question="2+2?",
            option_1="3",
            option_2="4",
            option_3="5",
            option_4="6",
            correct_option=2,
            explanation="2+2=4"
        )
        url = reverse('tests:test-check-answer')
        data = {"test_id": test.id, "selected_option": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_correct'])
