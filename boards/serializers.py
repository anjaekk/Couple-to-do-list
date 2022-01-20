from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Task

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    theme = serializers.IntegerField()
    title = serializers.CharField()
    contents = serializers.CharField()
    place = serializers.CharField()
    note  = serializers.CharField()
    is_done = serializers.CharField(default=False)

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    class Meta:
        model = Task
        fields = '__all__'