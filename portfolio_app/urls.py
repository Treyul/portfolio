from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/contact', views.api_contact, name='api_contact_noslash'),
    path('api/contact/', views.api_contact, name='api_contact'),
    re_path(r'^.*$', views.app_shell, name='app'),
]
