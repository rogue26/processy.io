from django.urls import path

from . import views

urlpatterns = [
    path('add_organization/', views.AddOrganization.as_view(), name='add_organization'),
    path('organization/', views.OrganizationDashboard.as_view(), name='organization'),
]
