from django.test import TestCase
from django.forms.models import model_to_dict

from blog.forms import PostForm, ThreadForm
from blog.factories import PostFactory, ThreadFactory


class PostFormTestCase(TestCase):
	def test_valid_basic_form(self):
		post = PostFactory.build()
		form = PostForm(data=model_to_dict(post))
		self.assertTrue(form.is_valid())


class ThreadFormTestCase(TestCase):
	def test_valid_basic_form(self):
		thread = ThreadFactory.build()
		form = ThreadForm(data=model_to_dict(thread))
		self.assertTrue(form.is_valid())
