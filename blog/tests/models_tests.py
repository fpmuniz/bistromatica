from django.test import TestCase

from blog.models import Post, Thread
from blog.factories import PostFactory, PublishedPostFactory, ThreadFactory


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
		posts = PublishedPostFactory.create_batch(3)
		for post in posts:
			self.thread.posts.add(post)
		self.assertEqual(self.thread.posts.count(), 3)

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


