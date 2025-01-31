from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status, permissions
from .serializers import UserRegistrationSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, TaskCompleteSerializer 
from .permissions import IsParent, IsKid
from .models import Behavior
from .serializers import BehaviorSerializer
from .models import Task
from .permissions import IsKid

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow access without authentication

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return HttpResponse("Welcome to TaskDown!")

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
        })
    
# Parent can create tasks
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def perform_create(self, serializer):
        serializer.save(parent=self.request.user)

# Kids can view their tasks
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsKid]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)
    
# Kid marks a task as completed
class TaskCompleteView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCompleteSerializer
    permission_classes = [IsAuthenticated, IsKid]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class BehaviorLogView(generics.CreateAPIView):
    queryset = Behavior.objects.all()
    serializer_class = BehaviorSerializer
    permission_classes = [IsAuthenticated, IsParent]

    def perform_create(self, serializer):
        serializer.save(logged_by=self.request.user)
