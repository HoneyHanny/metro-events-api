from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import generics, status

from .models import Event, Comment
from .serializers import UserSerializer, RegisterUserSerializer, MyTokenObtainPairSerializer, EventSerializer, \
    CommentSerializer
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


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


# # POST ONLY
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


class DeleteUser(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    """
        Utilizes the parent classes method to handle the functionality.
    """
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