from django.urls import path

from .views import add, configure, delete, ajax

app_name = 'modals'
urlpatterns = [
    path(r'add_organization/', add.AddOrganization.as_view(), name='add_organization'),
    path(r'add_project/', add.AddProject.as_view(), name='add_project'),
    path(r'add_workstream/<int:project_id>/', add.AddWorkstream.as_view(), name='add_workstream'),
    path(r'add_deliverable/<int:project_id>/', add.AddDeliverable.as_view(), name='add_deliverable'),
    path(r'add_task/<int:project_id>/', add.AddTask.as_view(), name='add_task'),
    path(r'add_workstream_type/', add.AddWorkstreamType.as_view(), name='add_workstream_type'),
    path(r'add_deliverable_type/', add.AddDeliverableType.as_view(), name='add_deliverable_type'),
    path(r'add_team_member/', add.AddTeamMember.as_view(), name='add_team_member'),
    path(r'add_task_type/', add.AddTaskType.as_view(), name='add_task_type'),
    path(r'add_content/', add.AddContent.as_view(), name='add_content'),
    path(r'add_content_type/', add.AddContentType.as_view(), name='add_content_type'),
    path(r'configure_workstream/<int:item_id>/', configure.ConfigureWorkstream.as_view(), name='configure_workstream'),
    path(r'configure_deliverable/<int:item_id>/', configure.ConfigureDeliverable.as_view(), name='configure_deliverable'),
    path(r'configure_task/<int:item_id>/', configure.ConfigureTask.as_view(), name='configure_task'),
    path(r'configure_team_member/<int:item_id>/', configure.ConfigureTeamMember.as_view(), name='configure_team_member'),
    path(r'delete_workstream/<int:item_id>/', delete.DeleteWorkstream.as_view(), name='delete_workstream'),
    path(r'delete_deliverable/<int:item_id>/', delete.DeleteDeliverable.as_view(), name='delete_deliverable'),
    path(r'delete_task/<int:item_id>/', delete.DeleteTask.as_view(), name='delete_task'),
    path(r'delete_team_member/<int:item_id>/', delete.DeleteTeamMember.as_view(), name='delete_team_member'),
    path(r'update_dropdown_options/', ajax.update_dropdown_options, name='update_dropdown_options'),
]
