from django.urls import path

from .views import ajax, ManageProjects, ProjectsDashboard, timeline_utilization

app_name = 'projects'
urlpatterns = [
    path(r'ajax/ajax-test/', ajax.ajax_test, name='ajax_test'),
    path(r'project/<int:project_id>', ProjectsDashboard.as_view(), name='project'),
    path(r'ajax/timeline_utilization', timeline_utilization, name='utilization_chart'),
    path(r'update_projects_table/', ajax.update_projects_table, name="update_projects_table"),
    path(r'update_workstreams_table/<int:project_id>/', ajax.update_workstreams_table, name="update_workstreams_table"),
    path(r'update_tasks_table/<int:project_id>/', ajax.update_tasks_table, name="update_tasks_table"),
    path(r'update_team_members_table/<int:project_id>/', ajax.update_team_members_table,
         name="update_team_members_table"),
    path(r'update_deliverables_table/<int:project_id>/', ajax.update_deliverables_table,
         name="update_deliverables_table"),
    path(r'', ManageProjects.as_view(), name='manage_projects'),
]
