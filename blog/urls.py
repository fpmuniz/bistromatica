from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('about/', views.about, name='about'),
    path('donate/', views.donate, name='donate'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('posts/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/publish/', views.PostPublishView.as_view(), name='post_publish'),
    path('posts/publish/', views.PostPublishView.as_view(), name='post_publish'),
    path('threads/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('threads/', views.ThreadListView.as_view(), name='thread_list'),
    path('', views.index, name='index'),
]
