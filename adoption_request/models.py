from django.db import models
from accounts.models import CustomUser
from pet.models import Pet


class AdoptionRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='adoption_requests')
    use_default_info = models.BooleanField(default=False)  # New field
    contact_info = models.TextField(blank=True, null=True)  # Optional if using default info-
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Use default contact info if requested
        if self.use_default_info and self.requester:
            self.contact_info = f"Email: {self.requester.email}, Phone: {self.requester.mobile}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Adoption Request by {self.requester.username} for {self.pet.name}"
