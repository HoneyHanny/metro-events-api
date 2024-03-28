from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Event, User
from .serializers import RegisterUserSerializer, UserSerializer, EventSerializer, UserSerializer

@api_view(["POST"])
def validate_register(request):

    if request.method != 'POST':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    user_serializer = RegisterUserSerializer(data=request.data)

    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = user_serializer.save()
    return Response(user_serializer.data, status=status.HTTP_201_CREATED)

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
    else:
        return Response({'error': 'GET method not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
def org_homepage(request):
    if request.method != 'GET':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    events = Event.objects.all()
    event_serializer = EventSerializer(events, many=True)
    return Response({'events': event_serializer.data}, status=status.HTTP_200_OK)

#
# === USERS ===
#

@api_view(['GET'])
def get_all_users(request):
    if request.method != 'GET':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    users = User.objects.all()

    if len(users) == 0:
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    users_serializer = UserSerializer(users, many=True)

    return Response({'users': users_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user(request, id):
    if request.method != 'GET':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    user = User.objects.get(pk=id)

    if user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user_serializer = UserSerializer(user)

    return Response({'user': user_serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_user(request, id):
    if request.method != 'PUT':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    old_user = User.objects.get(pk=id)

    if old_user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user_serializer = UserSerializer(instance=old_user, data=request.data)

    if not user_serializer.is_valid():
        return Response({'error': 'Invalid user'})

    user_serializer.save()

    return Response({'user': user_serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def remove_user(request, id):

    try:
        user = User.objects.get(pk=id)
    except:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.delete()

    return Response(None, status=status.HTTP_204_NO_CONTENT)

#
# === EVENTS ===
#

@api_view(['GET'])
def get_event(request, id):
    if request.method != 'GET':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        event = Event.objects.get(pk=id)
    except:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    event_serializer = EventSerializer(event)

    return Response({'user': event_serializer.data}, status=status.HTTP_200_OK)  # (OK) not tested yet

@api_view(['POST'])
def add_event(request):
    if request.method != 'POST':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    event_serializer = EventSerializer(data=request.data)
    
    if not event_serializer.is_valid():
        return Response({'error': 'Invalid event'}, status=status.HTTP_400_BAD_REQUEST)

    event_serializer.save()
    
    return Response({'event': event_serializer.data}, status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['PUT'])
def update_event(request, id):
    if request.method != 'PUT':
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        old_event = User.objects.get(pk=id)
    except:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    event_serializer = UserSerializer(instance=old_event, data=request.data)

    if not event_serializer.is_valid():
        return Response({'error': 'Invalid event'})

    event_serializer.save()

    return Response({'event': event_serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def remove_event(request, id):
    event = Event.objects.get(pk=id)

    if event is None:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    event.delete()

    return Response(None, status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET"])
# def getData(request):
#     person = {'name':'MetroEvents API Deploy Test', 'age':20}
#     return Response(person)
