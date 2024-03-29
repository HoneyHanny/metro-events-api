from .models import UserProfile, Event, Attendee
from rest_framework import serializers
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    message = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'message']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

    def validate(self, value):
        if User.objects.filter(username=value['username']).exists():
            raise serializers.ValidationError('Username is already in use')
        return value

    # instance refers to the model being serialized
    def to_representation(self, instance):

        data = super().to_representation(instance)
        # only display the message if create.
        if self.context.get('action') == 'create':
            data['message'] = "Success Register"
        return data

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