from django.urls import path
from . import views

urlpatterns = [
#   path('user/', views.getData),
  path('register/', views.validate_register), # add user
  path('login/', views.validate_login),
  path('homepage/', views.org_homepage), # get all events

  path('event/get/<int:id>/', views.get_event),
  path('event/add/', views.add_event),
  path('event/update/<int:id>/', views.update_event),
  path('event/remove/<int:id>/', views.remove_event),

  path('user/get/', views.get_all_users),
  path('user/get/<int:id>/', views.get_user),
  path('user/update/<int:id>/', views.update_user),
  path('user/remove/<int:id>/', views.remove_user),

  # sample usage
  # api-network/api/register
  # api-network/login
  # api-network/homepage

  # api-network/event/get/1
  # api-network/event/get
  # api-network/event/add
  # api-network/event/update/1
  # api-network/event/remove/1

  # api-network/user/get/
  # api-network/user/get/1
  # api-network/user/update/1
  # api-network/user/remove/1
]
