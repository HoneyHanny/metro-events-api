from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Event, Comment, Attendee, UserProfile, EventLikers
from .serializers import UserSerializer, RegisterUserSerializer, MyTokenObtainPairSerializer, EventSerializer, \
    CommentSerializer, AttendeeSerializer, EventLikersSerializer
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
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     return Response(status=status.HTTP_201_CREATED)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class SpecificEvent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    """
        Override, since we have custom requirement.
    """
    # def put(self, request, *args, **kwargs):
    #     event_id = kwargs.get('pk')
    #     try:
    #         event = Event.objects.get(pk=event_id)
    #         event.eventLikes += 1
    #         event.save()
    #         return Response(status=status.HTTP_200_OK)
    #     except Event.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]



class CommentListByEvent(generics.RetrieveDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"

    def get_queryset(self):
        event_id = self.kwargs.get('pk')
        return Comment.objects.filter(event_id=event_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JoinEvent(generics.ListCreateAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        try:

            # Gather all the information needed sa atong Attendee model.
            attendee_user = User.objects.filter(username=request.user).first()
            attendee_profile = UserProfile.objects.get(user=attendee_user)
            attendee_event = Event.objects.get(pk=event_id)

            # If existing si user ani nga event
            if Attendee.objects.filter(attendee=attendee_profile, events=attendee_event).exists():
                return Response({"error": "You have already joined this event."}, status=status.HTTP_400_BAD_REQUEST)

            event = Event.objects.get(pk=event_id)
            event.eventNumberOfAttendees += 1
            event.save()

            attendee = Attendee.objects.create(attendee=attendee_profile, events=attendee_event)

            # Serialize the Attendee object before including it in the response
            serializer = self.serializer_class(attendee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)

class EventLike(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventLikers.objects.all()
    serializer_class = EventLikersSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
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


# POST ONLY
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

    """
        Utilizes the parent classes method to handle the functionality.
    """

# [ 'GET', 'DELETE' ]
class DeleteUserByPk(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    """
        Utilizes the parent classes method to handle the functionality.
    """


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