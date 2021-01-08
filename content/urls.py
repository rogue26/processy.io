from django.urls import path

from . import views

app_name = 'content'
urlpatterns = [
    path('ajax/content-download/', views.ajax_content_download, name='ajax_content_download'),
    path('add_content_type/', views.AddContentType.as_view(), name='add_content_type'),
    path('add_content/', views.AddContent.as_view(), name='add_content'),
    path('content/', views.ContentDashboard.as_view(), name='content'),
]
