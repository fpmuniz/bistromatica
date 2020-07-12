import warnings
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.
class PostManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().exclude(visible=False)

class Post(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	published_at = models.DateTimeField(null=True, editable=False)
	title = models.CharField(max_length=256)
	content = RichTextField(blank=True)
	visible = models.BooleanField(default=False)
	thread = models.ForeignKey('Thread', on_delete=models.SET_NULL, null=True, blank=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)

	objects = PostManager()
	all_objects = models.Manager()

	def __str__(self):
		return self.title

	def __repr__(self):
		return f'Post <{self}>'

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		if self.visible and self.published_at is None:
			self.published_at = datetime.now()
		super().save(*args, **kwargs)


class Thread(models.Model):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)

	def get_absolute_url(self):
		return reverse('thread_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.name

	def __repr__(self):
		return f'Thread <{self}>'
