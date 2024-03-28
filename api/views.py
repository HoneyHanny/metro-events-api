from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Event
from .serializers import RegisterUserSerializer, UserSerializer, EventSerializer, UserProfileSerializer

@api_view(["POST"])
def validate_register(request):
    if request.method == "POST":
        user_serializer = RegisterUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST', 'GET'])
def validate_login(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            serializer = UserSerializer(user)
            return Response({"message": "Login Successful"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def org_homepage(request):
    if request.method == "GET":
        events = Event.objects.all()
        event_serializer = EventSerializer(events, many=True)
        return Response({'events': event_serializer.data})



@api_view(["GET"])
def getData(request):
    person = {'name':'MetroEvents API Deploy Test', 'age':20}
    return Response(person)
