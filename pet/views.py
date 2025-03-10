import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from accounts.permission import IsAuthorOrReadOnly, IsAdminOrReadOnly
from pet.models import Pet
from .serializers import PetSerializer
from rest_framework.decorators import action
from rest_framework import filters


class PetPagination(PageNumberPagination):
    page_size = 6


class PetFilter(django_filters.FilterSet):
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Case-insensitive search
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')  # Case-insensitive search
    author_username = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')  # Filter by author's username
    author_email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')  # Filter by author's email

    class Meta:
        model = Pet
        fields = ['gender', 'name', 'location', 'author_username', 'author_email']


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all().order_by('-date_added')
    serializer_class = PetSerializer
    pagination_class = PetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PetFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly | IsAdminOrReadOnly]
    search_fields = ['id', 'name', 'location', 'description', 'gender', 'author__username', 'author__email']

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

    # @action(detail=False, methods=['get'])
    # def pets_only(self, request):
    #     pets = Pet.objects.all()
    #     pets_without_exact_type = [pet for pet in pets if pet.get_pet_type() == "pets"]
    #
    #     page = self.paginate_queryset(pets_without_exact_type)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(pets_without_exact_type, many=True)
    #     return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pets_only(self, request):
        gender = request.query_params.get('gender', None)  # Get gender from query params

        # Get only base Pet instances (not Cat or Dog)
        pets = Pet.objects.filter(cat__isnull=True, dog__isnull=True)

        # Apply gender filtering if provided
        if gender:
            pets = pets.filter(gender__iexact=gender)  # Case-insensitive filter

        # Apply pagination
        page = self.paginate_queryset(pets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(pets, many=True)
        return Response(serializer.data)
