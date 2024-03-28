from collections import UserList

from django.urls import path
from . import views

urlpatterns = [
  path('user/', views.getData),
  path('register/', views.UserRegister.as_view()),
  path('login/', views.UserLogin.as_view()),
  # path('homepage/org/', views.org_homepage),
  # path('homepage/atnd/', views.atnd_homepage),
  path('users/<int:id>/', views.QueryUserByPk.as_view()),  # Use UsersList directly from views
  path('users/delete/<int:id>/', views.DeleteUserByPk.as_view())
]
