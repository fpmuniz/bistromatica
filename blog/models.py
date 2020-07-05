from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	published_at = models.DateTimeField(null=True, editable=False)
	title = models.CharField(max_length=256)
	content = models.TextField(blank=True)
