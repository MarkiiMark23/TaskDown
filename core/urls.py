from django.urls import path
from .views import home
from .views import UserRegistrationView
from .views import CustomAuthToken

urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
]
