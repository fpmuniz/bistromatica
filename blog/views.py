from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Thread
from .forms import PostForm, ThreadForm

# Create your views here.
class Index(RedirectView):
	url = reverse_lazy('post_list')


class About(TemplateView):
	template_name = 'blog/about.html'


class Donate(TemplateView):
	template_name = 'blog/donate.html'


class PostListView(RedirectView):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			self.url = reverse_lazy('post_full_list')
		else:
			self.url = reverse_lazy('post_public_list')
		return super().dispatch(request, *args, **kwargs)


class PublishedPostListView(ListView):
	queryset = Post.objects.order_by('-published_at')
	paginate_by = 10
	template_name = 'blog/post_list.html'


class AllPostsListView(LoginRequiredMixin, ListView):
	queryset = Post.all_objects.order_by('-published_at', '-created_at')
	paginate_by = 10
	template_name = 'blog/post_List.html'



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
