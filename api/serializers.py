from .models import UserProfile, Event, Attendee
from rest_framework import serializers
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class RegisterUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class AtndEventSerializer(serializers.ModelSerializer):
    eventOrganizer = UserProfileSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'eventName', 'eventVenue', 'eventDate', 'eventDescription', 'eventNumberOfAttendees',
                  'eventLikes', 'eventOrganizer']

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ('user',)

class EventAttendeesSerializer(serializers.ModelSerializer):
    attendees = AttendeeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'