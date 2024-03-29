
from django.urls import path
from . import views

urlpatterns = [
  path('user/', views.getData),
  path('register/', views.UserRegister.as_view()),
  path('login/', views.UserLogin.as_view()),
  # path('homepage/org/', views.org_homepage),
  # path('homepage/atnd/', views.atnd_homepage),
  path('users/<int:pk>/', views.QueryUserByPk.as_view()),  # Use UsersList directly from views
  path('users/delete/<int:pk>/', views.DeleteUserByPk.as_view()),
  path('users/delete/test/<int:pk>/', views.DeleteUser.as_view())
]
