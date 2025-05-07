from django.urls import path
from . import views

urlpatterns = [
    path('dash', views.admin_dashboard, name='admin_dashboard'),
]
