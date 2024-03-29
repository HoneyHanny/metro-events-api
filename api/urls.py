
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
  path('register/', views.UserRegister.as_view()),
  # path('login/', views.UserLogin.as_view()),
  # path('homepage/org/', views.org_homepage),
  # path('homepage/atnd/', views.atnd_homepage),
  path('users/<int:pk>/', views.QueryUserByPk.as_view()),  # Use UsersList directly from views
  path('users/delete/<int:pk>/', views.DeleteUserByPk.as_view()),
  path('users/delete/test/<int:pk>/', views.DeleteUser.as_view()),
  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('event/', views.EventList.as_view()),
  path('event/<int:pk>/', views.SpecificEvent.as_view()),
  path('comment/<int:pk>/', views.SpecificComment.as_view()),
  path('comment/', views.CommentList.as_view()),
]
