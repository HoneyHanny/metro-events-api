from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from .serializers import UserSerializer, AtndEventSerializer

# POST ONLY
class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(status=status.HTTP_201_CREATED)

# POST ONLY
class UserLogin(generics.CreateAPIView):
    serializer_class = UserSerializer  # Define the serializer class here

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login Successful"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# RetrieveAPIView is  used for querying single instance model given a primary-key.
class QueryUserByPk(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"


# [ 'GET', 'DELETE' ]
class DeleteUserByPk(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

# @api_view(["POST"])
# def validate_register(request):
#     if request.method == "POST":
#         user_serializer = RegisterUserSerializer(data=request.data)
#         if user_serializer.is_valid():
#             user = user_serializer.save()
#             return Response(user_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['POST', 'GET'])
# def validate_login(request):
#     if request.method == "POST":
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             serializer = UserSerializer(user)
#             return Response({"message": "Login Successful"}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def org_homepage(request):
#     if request.method == "GET":
#         events = Event.objects.all()
#         event_serializer = OrgEventSerializer(events, many=True)
#         return Response({'events': event_serializer.data})
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

@api_view(["GET"])
def getData(request):
    person = {'name':'MetroEvents API Deploy Test', 'age':20}
    return Response(person)
