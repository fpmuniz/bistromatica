from django.views.generic import ListView, DetailView

from blog.models import Thread


class ThreadDetailView(DetailView):
	model = Thread
	template_name = 'blog/thread_detail.html'


class ThreadListView(ListView):
	model = Thread
	template_name = 'blog/thread_list.html'
