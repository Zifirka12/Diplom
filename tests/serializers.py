from rest_framework import serializers
from .models import Answer, Question, Test, TestAttempt


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'explanation']
        extra_kwargs = {
            'is_correct': {'write_only': True},
            'explanation': {'write_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'points', 'order', 'answers']


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'passing_score', 
                 'created_at', 'updated_at', 'questions', 'questions_count']

    def get_questions_count(self, obj):
        return obj.questions.count()


class TestDetailSerializer(TestSerializer):
    class Meta(TestSerializer.Meta):
        fields = TestSerializer.Meta.fields + ['lesson']


class TestAttemptSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    test_title = serializers.SerializerMethodField()

    class Meta:
        model = TestAttempt
        fields = ['id', 'test', 'test_title', 'user', 'user_name', 'score',
                 'started_at', 'completed_at', 'is_completed']
        read_only_fields = ['user', 'score', 'completed_at', 'is_completed']

    def get_user_name(self, obj):
        return obj.user.get_full_name()

    def get_test_title(self, obj):
        return obj.test.title
