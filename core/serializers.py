from rest_framework import serializers
from .models import CustomUser
from .models import Task
from .models import Behavior

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'completed', 'parent', 'assigned_to']
        read_only_fields = ['parent']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_parent', 'is_kid']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            is_parent=validated_data.get('is_parent', False),
            is_kid=validated_data.get('is_kid', False),
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class BehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Behavior
        fields = ['id', 'behavior_type', 'description', 'date_logged', 'logged_by', 'associated_with']
        read_only_fields = ['logged_by', 'date_logged']