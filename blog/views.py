from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Thread
from .forms import PostForm, ThreadForm

# Create your views here.
def index(request):
	return HttpResponseRedirect('posts/')

def about(request):
	template = loader.get_template('blog/about.html')
	context = {}
	return HttpResponse(template.render(context, request))

def donate(request):
	template = loader.get_template('blog/donate.html')
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
	queryset = Post.all_objects.order_by('-published_at')
	template_name = 'blog/post_detail.html'


class PostFormView(LoginRequiredMixin, FormView):
	queryset = Post.all_objects.all()
	template_name = 'blog/post_form.html'
	form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
	queryset = Post.all_objects.all()
	template_name = 'blog/post_form.html'
	form_class = PostForm


class PostCreateView(LoginRequiredMixin, CreateView):
	queryset = Post.all_objects.all()
	template_name = 'blog/post_form.html'
	form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
	queryset = Post.all_objects.all()
	template_name = 'blog/post_delete.html'
	model = Post
	success_url = reverse_lazy('post_list')


class ThreadDetailView(DetailView):
	model = Thread
	template_name = 'blog/thread_detail.html'


class ThreadListView(ListView):
	model = Thread
	template_name = 'blog/thread_list.html'
