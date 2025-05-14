from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'tests', views.TestViewSet)
router.register(r'attempts', views.TestAttemptViewSet, basename='attempt')

tests_router = routers.NestedDefaultRouter(router, r'tests', lookup='test')
tests_router.register(r'questions', views.QuestionViewSet, basename='test-question')

questions_router = routers.NestedDefaultRouter(tests_router, r'questions', lookup='question')
questions_router.register(r'answers', views.AnswerViewSet, basename='question-answer')

app_name = 'tests'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tests_router.urls)),
    path('', include(questions_router.urls)),
]
