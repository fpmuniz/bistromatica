from django.views.generic import TemplateView, RedirectView
from django.urls import reverse_lazy


class Index(RedirectView):
	url = reverse_lazy('post_list')


class About(TemplateView):
	template_name = 'blog/about.html'


class Donate(TemplateView):
	template_name = 'blog/donate.html'
