from django.urls import path

from . import views

urlpatterns = [
    path('ajax/ajax-test/', views.ajax_test, name='ajax_test'),
    path('project/<int:project_id>', views.ProjectsDashboard.as_view(), name='project'),
    path('add_project', views.AddProject.as_view(), name='add_project'),
    path('utilization_chart', views.utilization_chart, name='utilization_chart'),
    path('', views.ManageProjects.as_view(), name='manage_projects'),
]
