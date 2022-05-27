from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import mailing
from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    title =  serializers.CharField(min_length=5)
    content = serializers.CharField(min_length=10)
    # Read-only fields are included in the API output, but should not be included in the input during create or update operations.
    user_name = serializers.ReadOnlyField(source='user_id.username')

    class Meta:
        model = Post
        fields = ['id', 'created_at', 'title', 'content', 'user_id', 'user_name']

class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'created_at', 'title', 'content']

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),message='The email you enter is already in use')]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),message='The username you enter is already in use')],
        min_length=8,
        max_length=50
    )

    password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        mailing.send_emails(validated_data)
        return user

class RetrieveUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']