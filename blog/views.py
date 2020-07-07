from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
	return HttpResponseRedirect('posts/')

def about(request):
	template = loader.get_template('blog/about.html')
	context = {}
	return HttpResponse(template.render(context, request))

class PostListView(ListView):
	queryset = Post.objects.order_by('-published_at')
	paginate_by = 10
	template_name = 'blog/post_list.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			self.queryset = Post.all_objects.order_by('-published_at')
			return super().get(request, *args, **kwargs)
		else:
			return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
	queryset = Post.objects.order_by('-published_at')
	template_name = 'blog/post_detail.html'

	def get(self, request, pk, *args, **kwargs):
		if request.user.is_authenticated:
			self.queryset = Post.all_objects.order_by('-published_at')
			return super().get(request, pk, *args, **kwargs)
		else:
			return super().get(request, pk, *args, **kwargs)


class PostEditView(LoginRequiredMixin, DetailView):
	queryset = Post.all_objects.all()
	template_name = 'blog/post_edit.html'
	publish = False

	def get(self, request, pk=None, *args, **kwargs):
		template = loader.get_template(self.template_name)
		if pk is None:
			user = User.objects.get(pk=request.user.pk)
			post = Post(creator=user)
		else:
			post = self.queryset.get(pk=pk)
		form = PostForm(instance=post)
		context = {'form': form, 'post': post}
		return HttpResponse(template.render(context, request))

	def post(self, request, pk=None, *args, **kwargs):
		if pk is None:
			post = Post()
			user = User.objects.get(pk=request.user.pk)
			post.creator = user
		else:
			post = self.queryset.get(pk=pk)
		post.title = request.POST['title']
		post.content = request.POST['content']
		if self.publish:
			post.publish()
		post.save()
		return HttpResponseRedirect(f'/posts/{post.pk}')


class PostPublishView(PostEditView):
	publish = True


class PostDeleteView(LoginRequiredMixin, DeleteView):
	queryset = PostEditView.queryset
	template_name = 'blog/post_delete.html'

	def post(self, request, pk, *args, **kwargs):
		post = self.queryset.get(pk=pk)
		post.delete()
		return HttpResponseRedirect('/posts/')
