from django.db import models
from accounts.models import CustomUser


class Pet(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    )
    name = models.CharField(max_length=50)
    year = models.SmallIntegerField(default=0)
    month = models.SmallIntegerField(default=0)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    adoption_cost = models.PositiveIntegerField(default=0)
    adoption_status = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image_1 = models.URLField()
    image_2 = models.URLField(blank=True, null=True)
    image_3 = models.URLField(blank=True, null=True)
    image_4 = models.URLField(blank=True, null=True)

    def get_pet_type(self):
        if hasattr(self, 'cat'):
            return 'cats'
        elif hasattr(self, 'dog'):
            return 'dogs'
        elif hasattr(self, 'bird'):
            return 'birds'
        return 'unknown'

    def __str__(self):
        return f"{self.name} - {self.id}"