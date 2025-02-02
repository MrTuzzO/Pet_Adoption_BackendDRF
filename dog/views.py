import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from accounts.permission import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Dog
from .serializers import DogSerializer
from cat.views import PetPagination


class DogFilter(django_filters.FilterSet):
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='iexact')
    color = django_filters.CharFilter(method='filter_colors')

    def filter_colors(self, queryset, name, value):
        # Split the colors by comma or spaces for multiple values
        colors = self.request.query_params.getlist('color')
        if colors:
            query = Q()
            for color in colors:
                query |= Q(colors__name__iexact=color)
            return queryset.filter(query).distinct()
        return queryset

    class Meta:
        model = Dog
        fields = ['gender', 'color']


class DogViewSet(viewsets.ModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    pagination_class = PetPagination  # If you have pagination setup
    filter_backends = [DjangoFilterBackend]
    filterset_class = DogFilter  # Use your custom filter class
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]  # Adjust permissions as needed

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)