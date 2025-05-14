from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

app_name = 'learning_platform'

# Основной роутер
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'tests', views.TestViewSet)
router.register(r'attempts', views.TestAttemptViewSet, basename='attempt')

# Вложенные роутеры
tests_router = routers.NestedDefaultRouter(router, r'tests', lookup='test')
tests_router.register(r'questions', views.QuestionViewSet, basename='test-questions')

questions_router = routers.NestedDefaultRouter(tests_router, r'questions', lookup='question')
questions_router.register(r'answers', views.AnswerViewSet, basename='question-answers')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tests_router.urls)),
    path('', include(questions_router.urls)),
] 