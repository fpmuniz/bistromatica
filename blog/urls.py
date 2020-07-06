from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('', views.index, name='index')
]
