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
	def test_publish(self):
		post = PostFactory.create()
		post.publish()
		self.assertIsNotNone(post.published_at)

	def test_unpublished_not_showing(self):
		post = PostFactory.create()
		self.assertEqual(Post.objects.count(), 0)
		self.assertEqual(Post.all_objects.count(), 1)
