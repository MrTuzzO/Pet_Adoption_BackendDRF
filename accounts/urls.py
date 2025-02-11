from django.urls import path
from .views import ProfileView, AdminStaffLoginView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('admin-login/', AdminStaffLoginView.as_view(), name='admin-login'),  # Custom login for admins
]