from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom User Model (Must be defined first)
class CustomUser(AbstractUser):
    is_parent = models.BooleanField(default=False)
    is_kid = models.BooleanField(default=False)

    def is_parent_user(self):
        return self.is_parent

    def is_kid_user(self):
        return self.is_kid

# Task Model
class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Right Now'),
    ]

    FUN_RATING_CHOICES = [
        (1, 'Sucked'),
        (2, 'Okay'),
        (3, 'Dont Care'),
        (4, 'Fun'),
        (5, 'Super Fun'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    completed = models.BooleanField(default=False)
    fun_rating = models.IntegerField(choices=FUN_RATING_CHOICES, null=True, blank=True)  # Rating 1-5
    time_taken = models.DurationField(null=True, blank=True)  # Time taken to finish
    did_not_finish = models.BooleanField(default=False)  # Task was not completed
    finished_late = models.BooleanField(default=False)  # Completed after due date
    not_quite = models.BooleanField(default=False)  # Partially completed

    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_tasks")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return f"{self.title} - {'Completed' if self.completed else 'Pending'}"

# Behavior Model
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

# Reward Model
class Reward(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    points_cost = models.PositiveIntegerField()
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rewards")
