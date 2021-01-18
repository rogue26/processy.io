from django.urls import path

from .views import RACI

app_name = 'RACI'
urlpatterns = [
    path(r'', RACI.as_view(), name='RACI'),
]
