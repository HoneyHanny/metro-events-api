
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
  path('register/', views.UserRegister.as_view()),
  # path('login/', views.UserLogin.as_view()),
  # path('homepage/org/', views.org_homepage),
  # path('homepage/atnd/', views.atnd_homepage),
  path('user/id/<str:username>', views.get_user_id),
  path('organizer/<int:pk>', views.Organizer.as_view()),
  path('users/<int:pk>/', views.QueryUserByPk.as_view()),  # Use UsersList directly from views
  path('users/delete/<int:pk>/', views.DeleteUserByPk.as_view()),
  # path('users/delete/test/<int:pk>/', views.DeleteUser.as_view()),
  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('event/', views.EventList.as_view()),
  # Ang ako approach sa join event kay inig click sa join button, dapat mo fetch siya og pk sa event
  # dayon kuhaon ang user gamit sa request.user since authenticted man ni siya.
  path('event/organizer/', views.ApprovedOrganizer.as_view()),
  path('event/create/', views.EventCreate.as_view()),
  path('event/<int:pk>/', views.SpecificEvent.as_view()),
  path('event/join/request/', views.JoinEventList.as_view()),
  path('event/join/request/<int:pk>/', views.JoinEvent.as_view()),
  path('event/join/request/response/<int:pk>/', views.JoinOrganizerResponse.as_view()),
  path('event/like/<int:eventLiked_id>/', views.EventLike.as_view()),
  path('event/comment/<int:event_id>/', views.CommentListByEventID.as_view()),
  path('event/comment/', views.CommentList.as_view()),
  path('event/notification/', views.UserNotifications.as_view()),
  path('event-notification/', views.UserNotificationsList.as_view())
]
