from django import forms

from .models import Post, Thread


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'


class ThreadForm(forms.ModelForm):
	class Meta:
		model = Thread
		fields = '__all__'
