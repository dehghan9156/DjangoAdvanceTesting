from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post
from django.views.generic.list import ListView
from django.views.generic import (
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response


class IndexView(TemplateView):
    """
    a class based view to show all posts
    """

    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["posts"] = Post.objects.all()
        return context


class PostListView(LoginRequiredMixin, ListView):
    # model = Post
    queryset = Post.objects.all()
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    # paginate_by = 2
    ordering = "-id"


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


# class PostCreateView(FormView):
#     template_name = 'blog/post_form.html'
#     form_class = PostForm
#     success_url = '/blog/post'
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    # fields = ['auther','title','content','published_date','status']
    success_url = "/blog/post"

    def form_valid(self, form):
        form.instance.auther = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post"


class PostDeleteView(DeleteView):
    model = Post
    success_url = "/blog/post"
    template_name = "blog/post_delete.html"
