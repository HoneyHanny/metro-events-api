from collections import UserList

from django.urls import path
from . import views

urlpatterns = [
  path('user/', views.getData),
  path('register/', views.UserRegister.as_view()),
  path('login/', views.UserLogin.as_view()),
  # path('homepage/org/', views.org_homepage),
  # path('homepage/atnd/', views.atnd_homepage),
  # path('users/', views.UsersList.as_view()),  # Use UsersList directly from views
]
