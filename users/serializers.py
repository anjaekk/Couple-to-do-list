from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers

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