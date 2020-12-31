from django.urls import path

from .views import AddWorkstream, AddWorkstreamType, ConfigureWorkstream, DeleteWorkstream

urlpatterns = [
    path('add_workstream/<int:project_id>/', AddWorkstream.as_view(), name='add_workstream'),
    path('add_workstream_type/', AddWorkstreamType.as_view(), name='add_workstream_type'),
    path('configure_workstream/<int:project_id>/<int:workstream_id>',
         ConfigureWorkstream.as_view(),
         name='configure_workstream'),
    path('delete_workstream/<int:project_id>/<int:pk>>', DeleteWorkstream.as_view(),
         name='delete_workstream'),
]
