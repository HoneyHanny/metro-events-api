from django.urls import path
from . import views

urlpatterns = [
  path('user/', views.getData),
  path('register/', views.validate_register),
  path('login/', views.validate_login),
  path('homepage/', views.org_homepage)
]
