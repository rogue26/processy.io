from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'organizations'
urlpatterns = [
    path('add_organization_modal/<slug:redirect_location>', views.AddOrganizationModal.as_view(), name='add_organization_modal'),
    path('add_division/', views.AddDivision.as_view(), name='add_division'),
    path('organization/', views.OrganizationDashboard.as_view(), name='organization'),
    url(r'update_declined_organization/', views.update_declined_organization, name="update_declined_organization"),
    url(r'update_type/', views.update_type, name="update_type"),
    url(r'add_type/', views.add_type, name="add_type"),
    url(r'delete_type/', views.delete_type, name="delete_type")
]
