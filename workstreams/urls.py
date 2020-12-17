from django.urls import path

from . import views

urlpatterns = [
    path('add_workstream/<int:project_id>/', views.AddWorkstream.as_view(), name='add_workstream'),
    path('add_workstream_type/', views.AddWorkstreamType.as_view(), name='add_workstream_type'),
    path('configure_workstream/<int:project_id>/<int:workstream_id>',
         views.ConfigureWorkstream.as_view(),
         name='configure_workstream'),
    path('delete_workstream/<int:project_id>/<int:pk>>', views.DeleteWorkstream.as_view(),
         name='delete_workstream'),
]
