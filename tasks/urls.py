from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('add_task_type/', views.AddTaskType.as_view(), name='add_task_type'),
    path('add_task/<int:project_id>/', views.AddTask.as_view(), name='add_task'),
    path('configure_task/<int:project_id>/<int:task_id>', views.ConfigureTask.as_view(), name='configure_task'),
    path('delete_task/<int:project_id>/<int:pk>>', views.DeleteTask.as_view(), name='delete_task'),
]
