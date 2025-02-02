from rest_framework import serializers
from .models import Cat, CatColor


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatColor
        fields = ['id', 'name']


class CatSerializer(serializers.ModelSerializer):
    color_names = serializers.SerializerMethodField()
    author_username = serializers.CharField(source='author.username', read_only=True)
    pet_type = serializers.SerializerMethodField()

    class Meta:
        model = Cat
        exclude = ['author']

    def get_color_names(self, obj):
        return [color.name for color in obj.colors.all()]

    def get_pet_type(self, obj):
        return obj.get_pet_type()

    def create(self, validated_data):
        colors_data = validated_data.pop('colors', None)
        request = self.context.get('request')  # Access the request object from the context
        validated_data['author'] = request.user  # Automatically set the author field
        cat = Cat.objects.create(**validated_data)  # Create the Cat instance

        if colors_data:
            cat.colors.set(colors_data)  # Associate colors if provided

        return cat

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
