from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register_user'),  # for registering a user
    path('login/', views.login, name='register_user'),  # for logging a user   
    path('tasks/', views.task_manager, name='task_manager'),  # All tasks (GET for list, POST for create) 
    path('refresh_token/', views.refresh_token, name='register_user'),  # for logging a user 
]