from django.db import models
from pet.models import Pet


class CatColor(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Cat(Pet):
    colors = models.ManyToManyField(CatColor, related_name="cats")
    food_habit = models.TextField()
    is_potty_trained = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.id}"