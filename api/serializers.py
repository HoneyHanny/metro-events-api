from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile, Event, Attendee, Comment, EventLikers, JoinRequest, Notification
from rest_framework import serializers

from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
class UserProfileSerializer(serializers.ModelSerializer):
    profile = UserSerializer(read_only=True)
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class EventSerializer(serializers.ModelSerializer):
    eventOrganizer = UserProfileSerializer(read_only=True)  # Nest UserProfileSerializer here

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        # Check if any event with the same organizer already exists on the given date
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


class JoinRequestSerializer(serializers.ModelSerializer):
    attendee = UserProfileSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    class Meta:
        model = JoinRequest
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserProfileSerializer(read_only=True)  # Serialize the recipient UserProfile

    class Meta:
        model = Notification
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        print(token)
        token['username'] = user.username

        return token



# class AtndEventSerializer(serializers.ModelSerializer):
#     eventOrganizer = UserProfileSerializer(read_only=True)
#     class Meta:
#         model = Event
#         fields = ['id', 'eventName', 'eventVenue', 'eventDate', 'eventDescription', 'eventNumberOfAttendees',
#                   'eventLikes', 'eventOrganizer']
#
# class AttendeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attendee
#         fields = ('user',)
#
# class EventAttendeesSerializer(serializers.ModelSerializer):
#     attendees = AttendeeSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Event
#         fields = '__all__'

