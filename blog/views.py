from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
	return HttpResponseRedirect('posts/')

class PostListView(ListView):
	model = Post
	paginate_by = 10
	template_name = 'blog/post_list.html'

	def get_queryset(self):
		return Post.objects.order_by('-published_at')


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'


class PostEditView(LoginRequiredMixin, DetailView):
	model = Post
	template_name = 'blog/post_edit.html'

	def get(self, request, pk=None, *args, **kwargs):
		template = loader.get_template('blog/post_edit.html')
		if pk is None:
			user = User.objects.get(pk=request.user.pk)
			post = Post(creator=user)
		else:
			post = Post.all_objects.get(pk=pk)
		form = PostForm(instance=post)
		context = {'form': form}
		return HttpResponse(template.render(context, request))
