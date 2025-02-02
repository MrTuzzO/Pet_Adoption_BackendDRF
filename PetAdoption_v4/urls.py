"""
URL configuration for PetAdoption_v4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import LoginView
from accounts.views import CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/login/', LoginView.as_view(), name='rest_login'),
    path('api/auth/registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Optional: For user registration
    path('api/pet/', include('cat.urls')),
    path('api/pet/', include('dog.urls')),
    path('api/', include('pet.urls')),
    path('api/adoptions/', include('adoption_request.urls')),  # Include adoptions app URLs
    path('api-auth/', include('rest_framework.urls')),  # For session-based login/logout in browsable API
    path("api/reports/", include("report.urls")),
]
