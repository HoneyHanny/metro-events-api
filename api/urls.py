from django.urls import path
from . import views

urlpatterns = [
#   path('user/', views.getData),
  path('register/', views.validate_register), # add user
  path('login/', views.validate_login),
  path('homepage/', views.org_homepage), # get all events

  path('event/<int:id>/', views.get_event),
  path('event/add/', views.add_event),
  path('event/update/<int:id>/', views.update_event),
  path('event/remove/<int:id>/', views.remove_event),

  path('users/', views.get_all_users),
  path('user/<int:id>/', views.get_user),
  path('user/update/<int:id>/', views.update_user),
  path('user/remove/<int:id>/', views.remove_user),
]
