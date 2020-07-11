import warnings
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class PostManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().exclude(published_at=None)

class Post(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	published_at = models.DateTimeField(null=True, editable=False)
	title = models.CharField(max_length=256)
	content = RichTextField(blank=True)
	thread = models.ForeignKey('Thread', on_delete=models.SET_NULL, null=True, blank=True)

	objects = PostManager()
	all_objects = models.Manager()

	class AlreadyPublishedWarning(RuntimeWarning):
		pass

	def publish(self):
		if self.published_at:
			w = self.AlreadyPublishedWarning(f'Trying to publish post "{self.title}", which has already been published.')
			warnings.warn(w)
			return
		self.published_at = datetime.now()

	def __str__(self):
		return self.title

	def __repr__(self):
		return f'Post <{self}>'


class Thread(models.Model):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)

	def __str__(self):
		return self.name

	def __repr__(self):
		return f'Thread <{self}>'
