import factory

from blog.models import Post
from .user_factory import UserFactory

class PostFactory(factory.DjangoModelFactory):
	class Meta:
		model = Post

	creator = factory.LazyFunction(UserFactory.create)
	title = factory.Faker('sentence')
	content = factory.Faker('text')


class PublishedPostFactory(PostFactory):
	visible = True
