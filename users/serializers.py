from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except ValidationError as err:
            raise serializers.ValidationError(str(err))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only":True}}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('Token is invalid or expired')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "password"]


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ["password"]


class FollowListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "name", "nickname"]


class UserDetailSerializer(serializers.ModelSerializer):
    follow_count = serializers.SerializerMethodField(method_name="get_follow_count")

    def get_follow_count(self, obj):
        follower_count = obj.follower.count()
        following_count = obj.following.count()
        return {"follower_count":follower_count, "following_count":following_count}

    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "name", "nickname", "follow_count"]