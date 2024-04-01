from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from .models import Event, Comment, Attendee, UserProfile, EventLikers, JoinRequest, Notification
from .serializers import UserSerializer, RegisterUserSerializer, MyTokenObtainPairSerializer, EventSerializer, \
    CommentSerializer, AttendeeSerializer, EventLikersSerializer, JoinRequestSerializer, NotificationSerializer, UserIdSerializer, OrganizerSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# TODO: Please ayaw pag erase og bisag isa nga comment. Thank you!
# POST ONLY
# Ako ge ukay ang mga parent classes unya their is no need for additional code.
class UserRegister(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    """
        Mo work ni nga code pero bad practice since pag check nako sa parent classes,
        ang CreateModelMixin, same implementation so ge utilize nako.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class SpecificEvent(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def put(self, request, *args, **kwargs):
    #     event_id = kwargs.get('pk')
    #     try:
    #         event = Event.objects.get(pk=event_id)
    #         event.eventLikes += 1
    #         event.save()
    #         return Response(status=status.HTTP_200_OK)
    #     except Event.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

# class CommentList(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]

class CommentListByEventID(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    lookup_field = "event_id"

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        return Comment.objects.filter(event_id=event_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        user = request.user
        comment = Comment.objects.create(comment=request.data['comment'], user=user, event_id=self.kwargs.get('event_id'))
        print(comment)
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)



class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


class JoinEvent(generics.CreateAPIView):
    serializer_class = JoinRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        try:
            attendee_user = User.objects.get(username=request.user)
            attendee_profile = UserProfile.objects.get(user=attendee_user)
            attendee_event = Event.objects.get(pk=event_id)

            # Check if the attendee already exists for this event
            if JoinRequest.objects.filter(attendee=attendee_profile, event=attendee_event).exists():
                return Response({"error": "You have already requested to join this event."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the join request
            join_request = JoinRequest.objects.create(attendee=attendee_profile, event=attendee_event)

            serializer = self.serializer_class(join_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return Response({"error": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response({"error": "User or UserProfile does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class JoinEventList(generics.ListAPIView):
    serializer_class = JoinRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Filter the join requests by events created by the authenticated user
        return JoinRequest.objects.filter(event__eventOrganizer__user=user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class JoinOrganizerResponse(generics.UpdateAPIView):
    queryset = JoinRequest.objects.all()
    serializer_class = JoinRequestSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        accepted = request.data.get('status')

        if accepted is None:
            return Response({"error": "Status field is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Update the status of the join request
                instance.is_accepted = accepted
                instance.save()

                # Create a notification for the user whose request was accepted or declined
                if accepted:
                    message = f"Your join request has been accepted for event: {instance.event.eventName}"
                else:
                    message = f"Your join request has been declined for event: {instance.event.eventName}"

                recipient_user = instance.attendee.user
                recipient_profile = UserProfile.objects.get(user=recipient_user)
                notification = Notification.objects.create(recipient=recipient_profile, message=message)
                instance.notification = notification
                instance.save()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the JoinRequest instance
        instance.delete()

        return Response({"message": "Join request response processed successfully."},
                        status=status.HTTP_200_OK)
class EventLike(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventLikers.objects.all()
    serializer_class = EventLikersSerializer
    permission_classes = [AllowAny]
    lookup_field = "eventLiked_id"

    def put(self, request, *args, **kwargs):
        event_id = kwargs.get("eventLiked_id")
        try:
            user = request.user
            liker_profile = UserProfile.objects.get(user=user)
            liked_event = Event.objects.get(pk=event_id)

            existing_like = EventLikers.objects.filter(likers=liker_profile, eventLiked=liked_event).first()

            if existing_like:
                existing_like.delete()
                liked_event.eventLikes -= 1
                liked_event.save()
                return Response({"message": "Like removed successfully."}, status=status.HTTP_200_OK)
            else:
                new_like = EventLikers.objects.create(likers=liker_profile, eventLiked=liked_event)
                liked_event.eventLikes += 1
                liked_event.save()
                # Save the new EventLikers instance to the database
                new_like.save()
                return Response({"message": "Event liked successfully."}, status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            return Response({"error": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)


class UserNotifications(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        username = self.request.user
        print(username)
        user = UserProfile.objects.get(user__username=self.request.user)
        return Notification.objects.filter(recipient__user_id=user.user_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)


class UserNotificationsList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

# class UserLogin(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#
#     """
#         create() for creating object. Although it is possible to use post() but iff (para nako) if you have specific
#         requirements.
#     """
#
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return Response({"message": "Login Successful"}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# RetrieveAPIView is  used for querying single instance model given a primary-key.

class QueryUserByPk(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    """
        Utilizes the parent classes method to handle the functionality.
    """

class Organizer(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [AllowAny]

# [ 'GET', 'DELETE' ]
class DeleteUserByPk(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs.get('pk'))
    """
        Override, since we have custom requirement.
    """

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class DeleteUser(generics.DestroyAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#     """
#         Utilizes the parent classes method to handle the functionality.
#     """
#
# @api_view(['GET'])
# def atnd_homepage(request):
#     if request.method == 'GET':
#         events = Event.objects.all()
#         event_serializer = AtndEventSerializer(events, many=True)
#         print(event_serializer)
#         return Response({'data': event_serializer.data}, status=status.HTTP_200_OK)
#     return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#

@api_view(['GET'])
def get_user_id(request, username):
    if request.method != 'GET':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        user = User.objects.get(username=username)
    except:
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user_serializer = UserIdSerializer(user)

    return Response({'user': user_serializer.data}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def create_event(request):
#     if request.method != 'POST':
#         return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     event_serializer = EventSerializer(data=request.data)
#
#     if not event_serializer.is_valid():
#         return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
#
#     # All of these commented code might be handled or catched by the previous check already
#     # try:
#     #     json_data = json.loads(request.body)
#     # except:
#     #     return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
#
#     # try:
#     #     User.objects.get(pk=json_data.eventOrganizer)
#     # except:
#     #     return Response({'error': 'Organizer not found or not a valid organizer'}, status=status.HTTP_400_BAD_REQUEST)
#
#     event_serializer.save()
#
#     return Response({'event': event_serializer.data}, status=status.HTTP_201_CREATED)
#