from rest_framework import serializers
from .models import Dog


class DogSerializer(serializers.ModelSerializer):
    color_names = serializers.SerializerMethodField()
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_user_img = serializers.CharField(source='author.user_img', read_only=True)
    pet_type = serializers.SerializerMethodField()

    class Meta:
        model = Dog
        exclude = ['author']

    def get_color_names(self, obj):
        return [color.name for color in obj.colors.all()]

    def get_pet_type(self, obj):
        return obj.get_pet_type()

    def create(self, validated_data):
        colors_data = validated_data.pop('colors')
        request = self.context.get('request')  # Access the request object from the context
        validated_data['author'] = request.user  # Automatically set the author field
        dog = Dog.objects.create(**validated_data)
        dog.colors.set(colors_data)  # Set colors using their IDs
        return dog

    def update(self, instance, validated_data):
        # Handle optional colors
        colors_data = validated_data.pop('colors', None)
        if colors_data is not None:
            instance.colors.set(colors_data)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
