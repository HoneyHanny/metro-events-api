from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile, Event, Attendee, Comment, EventLikers, JoinRequest, Notification, NonOrganizerEvent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class RegisterUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is already in use')
        return data

class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class EventSerializer(serializers.ModelSerializer):
    eventOrganizer = UserProfileSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        event_organizer = data.get('eventOrganizer')
        event_date = data.get('eventDate')
        if Event.objects.filter(eventOrganizer=event_organizer, eventDate=event_date).exists():
            raise serializers.ValidationError("An event by this organizer already exists on the same date.")
        return data

class CommentSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class AttendeeSerializer(serializers.ModelSerializer):
    attendee = UserProfileSerializer(read_only=True)
    events = EventSerializer(read_only=True)

    class Meta:
        model = Attendee
        fields = '__all__'

class EventLikersSerializer(serializers.ModelSerializer):
    likers = UserProfileSerializer(read_only=True)
    events = EventSerializer(read_only=True)

    class Meta:
        model = EventLikers
        fields = '__all__'

class NonOrganizerEventSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = NonOrganizerEvent
        fields = '__all__'

class JoinRequestSerializer(serializers.ModelSerializer):
    attendee = UserProfileSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = JoinRequest
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserProfileSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


