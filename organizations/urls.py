from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('add_organization_modal/<slug:redirect_location>', views.AddOrganizationModal.as_view(), name='add_organization_modal'),
    path('add_division/', views.AddDivision.as_view(), name='add_division'),
    path('organization/', views.OrganizationDashboard.as_view(), name='organization'),
    path('defaults/', views.DefaultsDashboard.as_view(), name='defaults'),
    url(r'update_declined_organization/', views.update_declined_organization, name="update_declined_organization")
]
