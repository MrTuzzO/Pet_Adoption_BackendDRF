from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pet, AdoptionRequest
from .serializers import AdoptionRequestSerializer, AdoptionRequestListSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from accounts.permission import IsAuthorOrReadOnly
from django.conf import settings
from django.core.mail import send_mail


class CreateAdoptionRequestView(generics.CreateAPIView):
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AdoptionRequest.objects.all()  # Add this line

    def perform_create(self, serializer):
        pet = Pet.objects.get(pk=self.kwargs['pet_id'])
        if pet.adoption_status:
            raise ValidationError("This pet has already been adopted.")
        if AdoptionRequest.objects.filter(pet=pet, requester=self.request.user).exists():
            raise ValidationError("You have already submitted a request for this pet.")
        if pet.author == self.request.user:
            raise ValidationError("You cannot submit an adoption request for yourself.")
        serializer.save(pet=pet, requester=self.request.user)

        # Send email notification
        email_subject = "🚨 New Adoption Request Submitted"
        email_body = f"""
                Dear {pet.author.username},

                A new adoption request has been submitted for your pet "{pet.name}".
                Please log in to your account to approve or reject this request.

                Best regards,  
                Pawgle
                """

        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [pet.author.email],
            fail_silently=False,
        )


class UpdateAdoptionRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            adoption_request_id = kwargs['id']
            action = request.data.get('action')  # 'approve' or 'reject'

            # Retrieve the adoption request
            adoption_request = AdoptionRequest.objects.get(id=adoption_request_id)

            # Check if the user is the pet's author
            if adoption_request.pet.author != request.user:
                return Response({"detail": "You are not authorized to manage this request."}, status=status.HTTP_403_FORBIDDEN)

            if action == 'approve':
                if adoption_request.status == 'Approved':
                    raise ValidationError("This request is already approved.")

                # Approve the adoption request
                adoption_request.status = 'Approved'
                adoption_request.save()

                # Send email notification for approval
                email_subject = "✅ Adoption Request Approved"
                email_body = f"""
                                Dear {adoption_request.requester.username},

                                Your adoption request for the pet "{adoption_request.pet.name}" has been approved!  
                                Please contact the pet's owner for further details.

                                Best regards,  
                                PAWGLE
                                """

                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [adoption_request.requester.email],
                    fail_silently=False,
                )

                # Reject all other requests for the same pet
                AdoptionRequest.objects.filter(pet=adoption_request.pet).exclude(id=adoption_request.id).update(status='Rejected')

                # Update pet's adoption status
                adoption_request.pet.adoption_status = True
                adoption_request.pet.save()

                # Send email notification for rejection
                email_subject = "Adoption Request Rejected"
                email_body = f"""
                                Dear {adoption_request.requester.username},

                                We regret to inform you that your adoption request for the pet "{adoption_request.pet.name}" has been rejected.  
                                Thank you for your understanding.

                                Best regards,  
                                PAWGLE
                                """

                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [adoption_request.requester.email],
                    fail_silently=False,
                )

                return Response({"message": "Adoption request approved successfully."}, status=status.HTTP_200_OK)

            elif action == 'reject':
                if adoption_request.status == 'Rejected':
                    raise ValidationError("This request is already rejected.")

                # Reject the adoption request
                adoption_request.status = 'Rejected'
                adoption_request.save()

                # Send email notification for rejection
                email_subject = "Adoption Request Rejected"
                email_body = f"""
                                Dear {adoption_request.requester.username},

                                We regret to inform you that your adoption request for the pet "{adoption_request.pet.name}" has been rejected.  
                                Thank you for your understanding.

                                Best regards,  
                                PAWGLE
                                """

                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [adoption_request.requester.email],
                    fail_silently=False,
                )

                return Response({"message": "Adoption request rejected successfully."}, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "Invalid action. Use 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)

        except AdoptionRequest.DoesNotExist:
            raise NotFound("Adoption request not found.")


class UserSentAdoptionRequestList(generics.ListAPIView):
    queryset = AdoptionRequest.objects.all().order_by('-date_requested')
    serializer_class = AdoptionRequestListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdoptionRequest.objects.filter(requester=self.request.user)


class UserReceivedAdoptionRequestList(generics.ListAPIView):
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdoptionRequest.objects.filter(pet__author=self.request.user)


class AdoptionRequestListView(generics.ListAPIView):
    serializer_class = AdoptionRequestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AdoptionRequest.objects.all()