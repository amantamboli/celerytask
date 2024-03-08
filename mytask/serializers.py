# serializers.py

from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    # url = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
