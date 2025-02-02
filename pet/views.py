from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from accounts.permission import IsAuthorOrReadOnly
from pet.models import Pet
from .serializers import PetSerializer
from rest_framework.decorators import action


class PetPagination(PageNumberPagination):
    page_size = 18


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    pagination_class = PetPagination

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_pets(self, request):
        user = request.user
        pets = Pet.objects.filter(author=user)

        # apply pagination
        page = self.paginate_queryset(pets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If pagination is not configured, return all results
        serializer = self.get_serializer(pets, many=True)
        return Response(serializer.data)