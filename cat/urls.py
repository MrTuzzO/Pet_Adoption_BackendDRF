from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatViewSet, ColorViewSet

router = DefaultRouter()
router.register(r'cats', CatViewSet, basename='cat')
router.register(r'colors', ColorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
