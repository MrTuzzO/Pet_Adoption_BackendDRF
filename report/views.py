from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]  # Allow all logged-in users to post
        elif self.action == "list":
            return [permissions.IsAuthenticated()]  # Allow all users to access (but restrict data)
        elif self.action in ["retrieve", "update"]:
            return [permissions.IsAdminUser()]  # Only admins can retrieve/update
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Report.objects.all().order_by('-created_at')  # Admins see all reports
        return Report.objects.filter(reporter=user).order_by('-created_at')  # Users see only their own reports

    def perform_create(self, serializer):
        report = serializer.save(reporter=self.request.user)

        email_subject = "🚨 New Report Submitted - Immediate Review Required"
        email_body = f"""
        Dear Admin,

        A new report has been submitted on the platform. Please review the details below:

        🔹 **Reported Post:** {report.post.name}  
        🔹 **Reported By:** {report.reporter.username} ({report.reporter.email})  
        🔹 **Reason:** {report.get_reason_display()}  
        🔹 **Description:** {report.description if report.description else "No additional details provided."}  
        🔹 **Submitted On:** {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}  

        🔍 **Action Required:** Please review and take necessary action in the admin panel.

        Best regards,  
        **Automated Notification System**  
        Pet Adoption Platform  
        """

        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        return Response({"message": "Your report has been submitted successfully. Our team will review it shortly."}, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        response = super().update(request, *args, **kwargs)
        instance.refresh_from_db()  # Refresh instance after update

        if instance.status != old_status:
            admin_feedback = instance.admin_feedback if instance.admin_feedback else "No additional feedback provided."

            email_subject = "📢 Report Status Update - Pet Adoption Platform"
            email_body = f"""
            Dear {instance.reporter.username},

            We hope you are doing well.

            Your report regarding the post **"{instance.post}"** has been **updated**. Below are the details:

            🔹 Report Status: {instance.status}  
            🔹 Reason for Report: {instance.get_reason_display()}  
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
                [instance.reporter.email],
                fail_silently=False,
            )
        return response