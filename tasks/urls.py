from django.urls import path
from . import views
print('inside the task url')

urlpatterns = [
    # All tasks (GET for list, POST for create) 
    path('', views.task_manager, name='task_manager'), 
    # single tasks, PUT AND DELETE
    path('<int:task_id>', views.task_detail, name='task_detail'), 
]