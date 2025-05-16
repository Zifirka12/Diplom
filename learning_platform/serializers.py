from rest_framework import serializers
from .models import Course, Lesson
from tests.serializers import TestSerializer


class LessonSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True, source='lesson_tests')
    tests_count = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'course', 'owner',
                 'created_at', 'updated_at', 'order', 'tests', 'tests_count']
        read_only_fields = ['owner']

    def get_tests_count(self, obj):
        return obj.lesson_tests.count()


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'owner', 'owner_name',
                 'created_at', 'updated_at', 'slug', 'lessons', 'lessons_count']
        read_only_fields = ['owner', 'slug']

    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None

    def get_lessons_count(self, obj):
        return obj.lessons.count()