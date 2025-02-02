from rest_framework import serializers
from pet.models import Pet


class PetSerializer(serializers.ModelSerializer):
    pet_type = serializers.SerializerMethodField()
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Pet
        fields = '__all__'

    def get_pet_type(self, obj):
        return obj.get_pet_type()