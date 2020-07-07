from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('posts/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/publish/', views.PostPublishView.as_view(), name='post_publish'),
    path('posts/publish/', views.PostPublishView.as_view(), name='post_publish'),
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
]
