from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('add_deliverable_type/', views.AddDeliverableType.as_view(), name='add_deliverable_type'),
    path('add_deliverable/<int:project_id>/', views.AddDeliverable.as_view(), name='add_deliverable'),
    path('configure_deliverable/<int:project_id>/<int:deliverable_id>',
         views.ConfigureDeliverable.as_view(),
         name='configure_deliverable'),
    path('delete_deliverable/<int:project_id>/<int:pk>>', views.DeleteDeliverable.as_view(),
         name='delete_deliverable'),
    url(r'update_spectype_condtype/', views.update_spectype_condtype, name="update_spectype_condtype"),
    url(r'add_spectype_condtype/', views.add_spectype_condtype, name="add_spectype_condtype"),
    url(r'delete_spectype_condtype/', views.delete_spectype_condtype, name="delete_spectype_condtype")
]
