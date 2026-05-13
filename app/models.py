from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )


class Project(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Task(models.Model):

    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=200)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    due_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title