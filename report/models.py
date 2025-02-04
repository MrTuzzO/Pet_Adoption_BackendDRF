from django.core.mail import send_mail
from django.db import models
from django.conf import settings
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

    # class Meta:
    #     unique_together = ("reporter", "post")

    def __str__(self):
        return f"{self.reporter.username} reported {self.post} for {self.get_reason_display()}"

    def save(self, *args, **kwargs):
        if self.pk:  # Check if this is an existing report (not a new one)
            old_instance = Report.objects.get(pk=self.pk)
            if old_instance.status != self.status:  # Status has changed
                admin_feedback = self.admin_feedback if self.admin_feedback else "No additional feedback provided."

                email_subject = "📢 Report Status Update - Pet Adoption Platform"
                email_body = f"""
                Dear {self.reporter.username},

                We hope you are doing well.

                Your report regarding the post **"{self.post}"** has been **updated**. Below are the details:

                🔹 Report Status: {self.status}  
                🔹 Reason for Report: {self.get_reason_display()}  
                🔹 Admin Feedback: {admin_feedback}  

                We appreciate your efforts in maintaining a safe and trustworthy platform.  
                If you have any further concerns, please feel free to reach out.

                Best regards,  
                **Support Team**  
                Pet Adoption Platform  
                {settings.DEFAULT_FROM_EMAIL}
                """

                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [self.reporter.email],
                    fail_silently=False,
                )

        super().save(*args, **kwargs)