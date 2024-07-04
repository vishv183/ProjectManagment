from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)