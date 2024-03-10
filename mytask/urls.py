from . import views

from django.urls import path,include
urlpatterns = [
    path('api/task/', views.TaskView.as_view(), name='task_api'),
    path('test/', views.test, name='test'),
    path('hello/', views.hello, name='hello'),
]