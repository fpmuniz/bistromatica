import factory
from django.test import TestCase

from django.contrib.auth.models import User
from .models import Post

# Create your tests here.
class UserFactory(factory.DjangoModelFactory):
	class Meta:
		model = User

	username = factory.Faker('user_name')
	password = factory.Faker('password')


class PostFactory(factory.DjangoModelFactory):
	class Meta:
		model = Post

	creator = factory.LazyFunction(UserFactory.create)
	title = factory.Faker('sentence')
	content = factory.Faker('text')

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
