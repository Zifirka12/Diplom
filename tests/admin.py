from django.contrib import admin
from .models import Test, Question, Answer, TestAttempt


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'question_type', 'points', 'order')
    list_filter = ('test', 'question_type')
    search_fields = ('text',)
    list_editable = ('points', 'order')
    inlines = [AnswerInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'passing_score', 'created_at')
    list_filter = ('lesson', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'started_at', 'completed_at', 'is_completed')
    list_filter = ('test', 'user', 'is_completed')
    search_fields = ('user__username', 'test__title')
    readonly_fields = ('started_at', 'completed_at')
