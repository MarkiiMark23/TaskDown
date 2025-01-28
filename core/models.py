from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_parent = models.BooleanField(default=False)
    is_kid = models.BooleanField(default=False)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    completed = models.BooleanField(default=False)
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assigned_tasks")
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")

class Behavior(models.Model):
    BEHAVIOR_TYPES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    ]
    behavior_type = models.CharField(choices=BEHAVIOR_TYPES, max_length=10)
    description = models.TextField()
    date_logged = models.DateTimeField(auto_now_add=True)
    logged_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="logged_behaviors")
    associated_with = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="behaviors")

class Reward(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    points_cost = models.PositiveIntegerField()
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rewards")
