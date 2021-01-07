from django.urls import path
from django.conf.urls import url

from .views import AddWorkstream, AddWorkstreamType, ConfigureWorkstream, DeleteWorkstream, ajax

urlpatterns = [
    path('add_workstream/<int:project_id>/', AddWorkstream.as_view(), name='add_workstream'),
    path('add_workstream_type/', AddWorkstreamType.as_view(), name='add_workstream_type'),
    path('configure_workstream/<int:project_id>/<int:workstream_id>',
         ConfigureWorkstream.as_view(),
         name='configure_workstream'),
    path('delete_workstream/<int:project_id>/<int:pk>>', DeleteWorkstream.as_view(),
         name='delete_workstream'),
    url(r'update_workstreams_table/<int:project_id>', ajax.update_workstreams_table, name="update_workstreams_table")
]
