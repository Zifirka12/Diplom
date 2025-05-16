from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group
from learning_platform.models import Course, Lesson
from .models import Test, Question, Answer
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class TestQuizTests(APITestCase):
    def setUp(self):
        # Создаем преподавателя
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='teachpass'
        )
        self.client.force_authenticate(user=self.teacher)
        self.course = Course.objects.create(name="Python", description="desc", owner=self.teacher)
        self.lesson = Lesson.objects.create(name="Intro", description="desc", course=self.course, owner=self.teacher)

    def test_create_test(self):
        test = Test.objects.create(
            lesson=self.lesson,
            title="Math Test",
            description="Basic arithmetic test",
            passing_score=70
        )
        self.assertEqual(test.title, "Math Test")
        self.assertEqual(test.lesson, self.lesson)
        self.assertEqual(test.passing_score, 70)
