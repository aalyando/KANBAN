from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('In QA', 'In QA'),
        ('Ready', 'Ready'),
        ('Done', 'Done'),
    )
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=100)
    status = models.CharField(choices=STATUS_CHOICES, default='New')
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'