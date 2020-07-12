from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('donate/', views.Donate.as_view(), name='donate'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/public/', views.PublishedPostListView.as_view(), name='post_public_list'),
    path('posts/all/', views.AllPostsListView.as_view(), name='post_full_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('threads/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('threads/', views.ThreadListView.as_view(), name='thread_list'),
]
