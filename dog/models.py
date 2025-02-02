from django.db import models
from pet.models import Pet
from cat.models import CatColor


class Dog(Pet):
    SIZE_CHOICES = (
        ('Tiny', 'Tiny (<5kg)'),
        ('Small', 'Small (5-10kg)'),
        ('Medium', 'Medium (10-25kg)'),
        ('Large', 'Large (25-45kg)'),
        ('Giant', 'Giant (>45kg)'),
    )
    colors = models.ManyToManyField(CatColor, related_name="dogs")
    food_habit = models.TextField()
    breed = models.CharField(max_length=50)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.id}"