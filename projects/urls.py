from django.urls import path

from . import views

urlpatterns = [
    path('ajax/ajax-test/', views.ajax_test, name='ajax_test'),
    path('project/<int:project_id>', views.ProjectsDashboard.as_view(), name='project'),
    path('defaults/', views.DefaultsDashboard.as_view(), name='defaults'),
    path('', views.ManageProjects.as_view(), name='manage_projects'),
]
