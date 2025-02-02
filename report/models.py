from django.db import models
from accounts.models import CustomUser
from pet.models import Pet


class Report(models.Model):
    REASON_CHOICES = [
        ("Fake", "Fake Content"),
        ("Irrelevant", "Irrelevant Post"),
        ("Violence", "Sensitive Violence"),
        ("Nudity", "Nudity or Sexual Content"),
        ("Other", "Other Issues"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending Review"),
        ("Reviewed", "Reviewed"),
        ("Rejected", "Rejected"),
    ]

    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports")
    post = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    admin_feedback = models.TextField(blank=True, null=True)  # Admin response

    class Meta:
        unique_together = ("reporter", "post")  # Prevent duplicate reports by the same user

    def __str__(self):
        return f"{self.reporter.username} reported {self.post} for {self.get_reason_display()}"