from django.urls import path
from . import views

urlpatterns = [
  path('user/', views.getData),
  path('user/<int:id>', views.getUser),
]
