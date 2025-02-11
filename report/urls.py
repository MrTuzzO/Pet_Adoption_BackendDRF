# from django.urls import path
# from .views import ReportViewSet
#
# urlpatterns = [
#     path("", ReportViewSet.as_view({"post": "create", "get": "list"}), name="report-list"),
#     path("<int:pk>/", ReportViewSet.as_view({"get": "retrieve", "patch": "update"}), name="report-detail"),
# ]


from rest_framework.routers import DefaultRouter
from .views import ReportViewSet

router = DefaultRouter()
router.register(r'', ReportViewSet, basename='report')

urlpatterns = router.urls