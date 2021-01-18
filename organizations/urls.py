from django.urls import path
from django.conf.urls import url

from .views import ajax, OrganizationDashboard, ContentDashboard

app_name = 'organizations'
urlpatterns = [
    path('organization/', OrganizationDashboard.as_view(), name='organization'),
    url(r'update_declined_organization/', ajax.update_declined_organization, name="update_declined_organization"),
    url(r'content_download/', ajax.content_download, name="content_download"),
    url(r'ajax_add_organization/', ajax.ajax_add_organization, name="ajax_add_organization"),
    url(r'add_workstream_type/', ajax.add_workstream_type, name="add_workstream_type"),
    url(r'add_deliverable_type/', ajax.add_deliverable_type, name="add_deliverable_type"),
    url(r'add_task_type/', ajax.add_task_type, name="add_task_type"),
    url(r'add_condition_type/', ajax.add_condition_type, name="add_condition_type"),
    url(r'add_specification_type/', ajax.add_specification_type, name="add_specification_type"),
    url(r'edit_workstream_type/', ajax.edit_workstream_type, name="edit_workstream_type"),
    url(r'edit_deliverable_type/', ajax.edit_deliverable_type, name="edit_deliverable_type"),
    url(r'edit_task_type/', ajax.edit_task_type, name="edit_task_type"),
    url(r'edit_condition_type/', ajax.edit_condition_type, name="edit_condition_type"),
    url(r'edit_specification_type/', ajax.edit_specification_type, name="edit_specification_type"),
    url(r'delete_workstream_type/', ajax.delete_workstream_type, name="delete_workstream_type"),
    url(r'delete_deliverable_type/', ajax.delete_deliverable_type, name="delete_deliverable_type"),
    url(r'delete_task_type/', ajax.delete_task_type, name="delete_task_type"),
    url(r'delete_condition_type/', ajax.delete_condition_type, name="delete_condition_type"),
    url(r'delete_specification_type/', ajax.delete_specification_type, name="delete_specification_type"),
    path('content/', ContentDashboard.as_view(), name='content'),
]
