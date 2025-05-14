from rest_framework import serializers
from .models import Test, Question, Answer, TestAttempt


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'explanation']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'test', 'text', 'question_type', 'points', 'order', 'answers']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'lesson', 'title', 'description', 'passing_score', 'created_at']


class TestDetailSerializer(TestSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(TestSerializer.Meta):
        fields = TestSerializer.Meta.fields + ['questions']


class TestAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttempt
        fields = ['id', 'test', 'user', 'score', 'started_at', 'completed_at', 'is_completed']
        read_only_fields = ['user', 'score', 'started_at', 'completed_at', 'is_completed']
