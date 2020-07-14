from datetime import datetime

import factory
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms.models import model_to_dict

from .models import Post, Thread
from .forms import PostForm, ThreadForm

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

	def test_html_basic_sanitizing(self):
		post = PostFactory.create(content='an <script>evil()</script> example')
		post.save()
		sanitized = 'an &lt;script&gt;evil()&lt;/script&gt; example'
		self.assertEqual(post.content, sanitized)

	def test_html_sanitizing_allows_text_content(self):
		content = '<p>text</p><h1>title</h1>'
		post = PostFactory.create(content=content)
		post.save()
		self.assertEqual(post.content, content)

	def test_html_sanitizing_allows_images(self):
		content = '<img alt="Imagem" src="/bla/">'
		post = PostFactory.create(content=content)
		post.save()
		self.assertEqual(post.content, content)

	def test_repr(self):
		try:
			self.post.__repr__()
		except BaseException as e:
			self.fail(f'{e} was raised.')

	def test_str(self):
		try:
			self.post.__str__()
		except BaseException as e:
			self.fail(f'{e} was raised.')


class ThreadTestCase(TestCase):
	def setUp(self):
		self.thread = ThreadFactory.create()

	def test_simple_thread(self):
		PublishedPostFactory.create_batch(3, thread=self.thread)
		self.assertEqual(self.thread.post_set.count(), 3)

	def test_repr(self):
		try:
			self.thread.__repr__()
		except BaseException as e:
			self.fail(f'{e} was raised.')

	def test_str(self):
		try:
			self.thread.__str__()
		except BaseException as e:
			self.fail(f'{e} was raised.')


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


class PostFormTestcase(TestCase):
	def test_valid_basic_form(self):
		post = PostFactory.build()
		form = PostForm(data=model_to_dict(post))
		self.assertTrue(form.is_valid())


class ThreadFormTestcase(TestCase):
	def test_valid_basic_form(self):
		thread = ThreadFactory.build()
		form = ThreadForm(data=model_to_dict(thread))
		self.assertTrue(form.is_valid())


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
		post = PostFactory.build()
		data = model_to_dict(post)
		data.pop('id')
		response = self.client.post(reverse('post_create'), data)
		self.assertEqual(Post.all_objects.count(), 1)

	def test_delete_post_redirect_login(self):
		post = PostFactory.create()
		response = self.client.post(reverse('post_delete', kwargs={'pk': post.pk}))
		self.assertEqual(response.status_code, 302)
		self.assertIn('login', response.url)
		self.assertEqual(Post.all_objects.count(), 1)

	def test_delete_post_authenticated(self):
		self.client.force_login(self.user)
		post = PostFactory.create()
		response = self.client.post(reverse('post_delete', kwargs={'pk': post.pk}))
		self.assertEqual(Post.all_objects.count(), 0)

	def test_update_post_authenticated(self):
		self.client.force_login(self.user)
		post = PostFactory.create()
		data = model_to_dict(post)
		data['content'] = "new content"
		response = self.client.post(reverse('post_update', kwargs={'pk': post.pk}), data)
		post.refresh_from_db()
		self.assertEqual(post.content, "new content")

	def test_update_post_redirect_login(self):
		post = PostFactory.create()
		data = model_to_dict(post)
		data['content'] = "new content"
		response = self.client.post(reverse('post_update', kwargs={'pk': post.pk}), data)
		post.refresh_from_db()
		self.assertNotEqual(post.content, "new content")

