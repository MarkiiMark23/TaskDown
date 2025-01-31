from django.urls import path
from .views import home
from .views import UserRegistrationView
from .views import CustomAuthToken
from .views import TaskCreateView, TaskListView
from .views import BehaviorLogView

urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('tasks/create/', TaskCreateView.as_view(), name='create-task'),
    path('tasks/', TaskListView.as_view(), name='list-tasks'),
    path('behaviors/log/', BehaviorLogView.as_view(), name='log-behavior'),
]
