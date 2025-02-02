from django.urls import path
from .views import UpdateAdoptionRequestView, CreateAdoptionRequestView, AdoptionRequestListView, UserSentAdoptionRequestList, UserReceivedAdoptionRequestList

urlpatterns = [
    path('adoption-request/', AdoptionRequestListView.as_view(), name='adoption-request-list'),
    path('adoption-request/<int:pet_id>/create/', CreateAdoptionRequestView.as_view(), name='create-adoption-request'),
    path('adoption-request/<int:id>/update/', UpdateAdoptionRequestView.as_view(), name='update-adoption-request'),
    path('adoption-request/sent-requests/', UserSentAdoptionRequestList.as_view(), name='user_adoption_requests'),
    path('adoption-request/received-requests/', UserReceivedAdoptionRequestList.as_view(), name='user_received_adoption_requests')
]
