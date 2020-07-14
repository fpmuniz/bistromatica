import warnings
from datetime import datetime
import re

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
import bleach

# Create your models here.

# HTML sanitizer whitelists
class Whitelist:
	tags = bleach.sanitizer.ALLOWED_TAGS.copy()
	tags += ['p', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'cite', 'br']
	attrs = bleach.sanitizer.ALLOWED_ATTRIBUTES.copy()
	attrs.setdefault('img', [])
	attrs['img'] += ['src', 'alt']
	attrs.setdefault('p', [])
	attrs['p'] += ['style']
	styles = bleach.sanitizer.ALLOWED_STYLES.copy()
	styles += ['color', 'background-color', 'text-align']

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

	PARAGRAPH_PATTERN = re.compile(r'<p.*?>.*?</p>', flags=re.MULTILINE)

	def __str__(self):
		return self.title

	def __repr__(self):
		return f'Post <{self}>'

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk})

	def clean_html(self):
		print(self.content[:1000])
		self.content = bleach.clean(self.content, tags=Whitelist.tags, attributes=Whitelist.attrs, styles=Whitelist.styles)
		print('-'*80)
		print(self.content[:1000])

	def save(self, *args, **kwargs):
		if self.visible and self.published_at is None:
			self.published_at = datetime.now()
		self.clean_html()
		super().save(*args, **kwargs)

	@property
	def preview(self):
		pat = self.PARAGRAPH_PATTERN
		match = pat.finditer(self.content)
		if not match: return
		out = []
		for i, text in enumerate(match):
			if i >= 3: break
			out.append(text[0])
		return ''.join(out)


class Thread(models.Model):
	name = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)

	def get_absolute_url(self):
		return reverse('thread_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.name

	def __repr__(self):
		return f'Thread <{self}>'
