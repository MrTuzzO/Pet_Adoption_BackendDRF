from django.urls import path
from .views import ReportViewSet

urlpatterns = [
    path("", ReportViewSet.as_view({"post": "create", "get": "list"}), name="report-list"),
    path("<int:pk>/", ReportViewSet.as_view({"get": "retrieve", "patch": "update"}), name="report-detail"),
]
