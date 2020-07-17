import factory

from blog.models import Thread


class ThreadFactory(factory.DjangoModelFactory):
	class Meta:
		model = Thread

	name = factory.Faker('sentence')
	description = factory.Faker('text')