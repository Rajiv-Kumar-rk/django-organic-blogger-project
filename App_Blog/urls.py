from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('create-blog/', views.CreateBlog.as_view(), name='create_blog'),
   path('my-blogs/', views.MyBlogs.as_view(), name='my_blogs'),
   path('blog-details/<str:slug>/', views.blog_details, name='blog_details'),
   path('edit-blog/<pk>/', views.EditBlog.as_view() , name='edit_blog'),
   path('delete-blog/<pk>/', views.delete_blog, name='delete_blog'),
   path('like-blog/<pk>/', views.like_blog, name='like_blog'),
   path('dislike-blog/<pk>/', views.dislike_blog, name='dislike_blog'),
]
