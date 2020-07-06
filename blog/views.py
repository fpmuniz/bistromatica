from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect

from .models import Post

# Create your views here.
def index(request):
	return HttpResponseRedirect('posts/')

class PostListView(ListView):
	model = Post
	paginate_by = 10
	template_name = 'blog/index.html'

	def get_queryset(self):
		return Post.objects.order_by('published_at')
