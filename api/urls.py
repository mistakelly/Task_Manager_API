from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register_user'),  # for registering a user
    path('login/', views.login, name='register_user'),  # for logging a user    
]