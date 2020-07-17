from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


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
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	threads = models.ManyToManyField('Thread', related_name='posts', through='ThreadItem')

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
