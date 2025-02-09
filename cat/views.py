import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from accounts.permission import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from pet.views import PetPagination
from .models import Cat, CatColor
from .serializers import CatSerializer, ColorSerializer
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet


class CatFilter(django_filters.FilterSet):
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
        model = Cat
        fields = ['gender', 'color']


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all().order_by('-date_added')
    serializer_class = CatSerializer
    pagination_class = PetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CatFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ColorViewSet(ModelViewSet):
    queryset = CatColor.objects.all()
    serializer_class = ColorSerializer