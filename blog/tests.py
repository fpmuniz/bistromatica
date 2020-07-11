from datetime import datetime

import factory
from django.test import TestCase
from django.contrib.auth.models import User

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


class PostTestCase(TestCase):
	def setUp(self):
		self.post = PostFactory.create()

	def test_publish(self):
		self.post.publish()
		self.assertIsNotNone(self.post.published_at)

	def test_unpublished_not_showing(self):
		self.assertEqual(Post.objects.count(), 0)
		self.assertEqual(Post.all_objects.count(), 1)

	def test_publish_twice_warns(self):
		self.post.publish()
		with self.assertWarns(self.post.AlreadyPublishedWarning):
			self.post.publish()

class ThreadTestCase(TestCase):
	def setUp(self):
		self.thread = ThreadFactory.create()

	def test_simple_thread(self):
		PublishedPostFactory.create_batch(3, thread=self.thread)
		self.assertEqual(self.thread.post_set.count(), 3)
