from rest_framework import serializers
from .models import AdoptionRequest


class AdoptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        fields = [
            'id',
            'pet',
            'use_default_info',
            'contact_info',
            'message',
            'status',
            'date_requested',
        ]
        read_only_fields = ['status', 'date_requested']


class AdoptionRequestListSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    author = serializers.CharField(source='pet.author', read_only=True)
    requester = serializers.CharField(source='requester.username', read_only=True)  # Add this field

    class Meta:
        model = AdoptionRequest
        fields = ['id', 'pet_name', 'requester','contact_info', 'message', 'status', 'date_requested', 'date_updated', 'author']