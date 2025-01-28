from django.urls import path
from .views import home
from .views import UserRegistrationView

urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
