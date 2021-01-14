from django.urls import path
from django.conf.urls import url

from .views import ajax, OrganizationDashboard, ContentDashboard

app_name = 'organizations'
urlpatterns = [
    path('organization/', OrganizationDashboard.as_view(), name='organization'),
    url(r'update_declined_organization/', ajax.update_declined_organization, name="update_declined_organization"),
    url(r'update_type/', ajax.update_type, name="update_type"),
    url(r'add_type/', ajax.add_type, name="add_type"),
    url(r'delete_type/', ajax.delete_type, name="delete_type"),
    url(r'content_download/', ajax.content_download, name="content_download"),
    url(r'ajax_add_organization/', ajax.ajax_add_organization, name="ajax_add_organization"),
    url(r'ajax_add_deliverable_type/', ajax.ajax_add_deliverable_type, name="ajax_add_deliverable_type"),
    path('content/', ContentDashboard.as_view(), name='content'),
]
