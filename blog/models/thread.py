from django.urls import reverse
from django.db import models


class Thread(models.Model):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)

	def get_absolute_url(self):
		return reverse('thread_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.name

	def __repr__(self):
		return f'Thread <{self}>'
