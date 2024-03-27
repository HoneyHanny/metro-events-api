from django.urls import path
from . import views

urlpatterns = [
  path('user/', views.getData),
  path('register/', views.validate_register),
]
