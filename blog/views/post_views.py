from django.urls import reverse_lazy
from django.views.generic import RedirectView, ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post
from blog.forms import PostForm


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

	def form_valid(self, form):
		form.instance.creator = self.request.user
		return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
	queryset = Post.all_objects.all()
	template_name = 'blog/post_delete.html'
	model = Post
	success_url = reverse_lazy('post_list')
