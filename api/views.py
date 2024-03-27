from .models import UserProfile
from django.views.decorators.http import require_POST
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status



@api_view(["GET"])
def getData(request):
    person = {'name':'MetroEvents API Deploy Test', 'age':20}
    return Response(person)


@api_view(["POST"])
def validate_register(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

