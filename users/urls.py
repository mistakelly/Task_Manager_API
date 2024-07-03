from django.urls import path
from . import views


urlpatterns = [
    # FOR GETTING ALL USERS
    path('', views.get_users, name='get_users'),  

    # FOR GETING A SINGLE USER
    path('<int:id>/', views.get_user, name='get_users'),  

    # FOR REGISTERING USER
    path('register/', views.register, name='register_user'),  

    # FOR AUTHENTICATING USER
    path('login/', views.login, name='register_user'),   

    # REFRESHING USERS TOKEN
    path('refresh_token/', views.refresh_token, name='register_user'),  
]