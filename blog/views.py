from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect

from .models import Post

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


class PostEditView(DetailView):
	model = Post
	template_name = 'blog/post_edit.html'
