from django.urls import path

from . import views

urlpatterns = [
    path('add_content_type/', views.AddContentType.as_view(), name='add_content_type'),
    path('add_content/', views.AddContent.as_view(), name='add_content'),
    path('content/', views.ContentDashboard.as_view(), name='content'),
]
