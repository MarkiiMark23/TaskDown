from rest_framework import serializers
from .models import CustomUser

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
