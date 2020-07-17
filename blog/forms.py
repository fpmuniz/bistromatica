from django import forms

from .models import Post, Thread


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'content', 'visible']


class ThreadForm(forms.ModelForm):
	class Meta:
		model = Thread
		fields = ['name', 'description']
