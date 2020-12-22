from django.urls import path

from . import views

urlpatterns = [
    path('add_team_member/<int:project_id>/', views.AddTeamMember.as_view(), name='add_team_member'),
    path('configure_team_member/<int_team_member_id>/', views.ConfigureTeamMember.as_view(), name='configure_team_member'),
]
