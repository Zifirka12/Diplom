from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Prefetch

from .models import Course, Lesson
from tests.models import Test, Question, Answer, TestAttempt
from .serializers import CourseSerializer, LessonSerializer
from tests.serializers import (
    TestSerializer, TestDetailSerializer, QuestionSerializer,
    AnswerSerializer, TestAttemptSerializer
)
from .permissions import IsOwnerOrReadOnly, IsTeacherOrAdmin, CanManageTests, CanTakeTest


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        if self.request.user.groups.filter(name="teachers").exists():
            return queryset.filter(owner=self.request.user)
        return queryset.filter(lessons__isnull=False).distinct()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        if self.request.user.groups.filter(name="teachers").exists():
            return queryset.filter(owner=self.request.user)
        return queryset.filter(course__isnull=False)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, CanManageTests]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestDetailSerializer
        return TestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        if self.request.user.groups.filter(name="teachers").exists():
            return queryset.filter(lesson__owner=self.request.user)
        return queryset.filter(lesson__course__isnull=False)

    @action(detail=True, methods=['post'], permission_classes=[CanTakeTest])
    def start_attempt(self, request, pk=None):
        test = self.get_object()
        attempt = TestAttempt.objects.create(
            test=test,
            user=request.user
        )
        return Response(TestAttemptSerializer(attempt).data)

    @action(detail=True, methods=['post'], permission_classes=[CanTakeTest])
    def submit_attempt(self, request, pk=None):
        test = self.get_object()
        try:
            attempt = TestAttempt.objects.get(
                test=test,
                user=request.user,
                is_completed=False
            )
        except TestAttempt.DoesNotExist:
            return Response(
                {"error": "Активная попытка не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверка ответов
        answers = request.data.get('answers', {})
        total_points = 0
        max_points = 0

        for question in test.questions.all():
            max_points += question.points
            if str(question.id) in answers:
                if question.question_type == 'text':
                    # Для текстовых ответов проверяем точное совпадение
                    correct_answer = question.answers.filter(is_correct=True).first()
                    if correct_answer and answers[str(question.id)].lower() == correct_answer.text.lower():
                        total_points += question.points
                else:
                    # Для выбора одного или нескольких вариантов
                    correct_answers = set(question.answers.filter(is_correct=True).values_list('id', flat=True))
                    user_answers = set(map(int, answers[str(question.id)] if isinstance(answers[str(question.id)], list) else [answers[str(question.id)]]))
                    if correct_answers == user_answers:
                        total_points += question.points

        # Вычисление процента правильных ответов
        score = (total_points / max_points * 100) if max_points > 0 else 0

        # Обновление попытки
        attempt.score = score
        attempt.completed_at = timezone.now()
        attempt.is_completed = True
        attempt.save()

        return Response({
            'score': score,
            'passing_score': test.passing_score,
            'passed': score >= test.passing_score
        })


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, CanManageTests]

    def get_queryset(self):
        test_id = self.kwargs.get('test_pk')
        if test_id:
            return Question.objects.filter(test_id=test_id)
        return Question.objects.none()


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, CanManageTests]

    def get_queryset(self):
        question_id = self.kwargs.get('question_pk')
        if question_id:
            return Answer.objects.filter(question_id=question_id)
        return Answer.objects.none()


class TestAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TestAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return TestAttempt.objects.all()
        if self.request.user.groups.filter(name="teachers").exists():
            return TestAttempt.objects.filter(test__lesson__owner=self.request.user)
        return TestAttempt.objects.filter(user=self.request.user) 