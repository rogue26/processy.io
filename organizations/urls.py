from django.urls import path

from . import views

urlpatterns = [
    path('add_organization/', views.AddOrganization.as_view(), name='add_organization'),
    path('add_division/<int:organization_id>', views.AddDivision.as_view(), name='add_division'),
    path('organization/', views.OrganizationDashboard.as_view(), name='organization'),
]
