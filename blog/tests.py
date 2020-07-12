from datetime import datetime

import factory
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Post, Thread

# Create your tests here.
class UserFactory(factory.DjangoModelFactory):
	class Meta:
		model = User

	username = factory.Faker('user_name')
	password = factory.Faker('password')


class ThreadFactory(factory.DjangoModelFactory):
	class Meta:
		model = Thread

	name = factory.Faker('sentence')
	description = factory.Faker('text')


class PostFactory(factory.DjangoModelFactory):
	class Meta:
		model = Post

	creator = factory.LazyFunction(UserFactory.create)
	thread = factory.LazyFunction(ThreadFactory.create)
	title = factory.Faker('sentence')
	content = factory.Faker('text')


class PublishedPostFactory(PostFactory):
	published_at = factory.LazyFunction(datetime.now)
	visible = True


class PostTestCase(TestCase):
	def setUp(self):
		self.post = PostFactory.create()

	def test_publish(self):
		self.post.visible = True
		self.post.save()
		self.assertIsNotNone(self.post.published_at)

	def test_unpublished_not_showing(self):
		self.assertEqual(Post.objects.count(), 0)
		self.assertEqual(Post.all_objects.count(), 1)



class ThreadTestCase(TestCase):
	def setUp(self):
		self.thread = ThreadFactory.create()

	def test_simple_thread(self):
		PublishedPostFactory.create_batch(3, thread=self.thread)
		self.assertEqual(self.thread.post_set.count(), 3)

class TemplateViewTestCase(TestCase):
	def test_index(self):
		response = self.client.get(reverse('index'))
		self.assertLess(response.status_code, 400)

	def test_about(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)

	def test_donate(self):
		response = self.client.get(reverse('donate'))
		self.assertEqual(response.status_code, 200)


class PostViewTestCase(TestCase):
	def setUp(self):
		self.user = UserFactory.create()

	def test_post_list_redirect_published_only_when_not_logged_in(self):
		response = self.client.get(reverse('post_list'))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('post_public_list'))

	def test_post_list_redirects_to_all_posts_when_logged_in(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse('post_list'))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('post_full_list'))

	def test_redirect_post_creation_to_anon_user(self):
		response = self.client.get(reverse('post_create'))
		self.assertEqual(response.status_code, 302)

	def test_get_create_post(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse('post_create'))
		self.assertEqual(response.status_code, 200)

	def test_create_post(self):
		self.client.force_login(self.user)
		response = self.client.post(reverse('post_create'))
		self.assertEqual(response.status_code, 200)
