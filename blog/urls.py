from django.urls import path
from . import views

urlpatterns = [
path("blog/", views.Blog_list, name="blog_list"),
path("detail/<int:id>/", views.blog_detail, name="blog_detail"),
path("rate/", views.blog_rate, name="blog_rate"),
path("comment/", views.blog_comment, name="blog_comment")
]