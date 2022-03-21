from django.shortcuts import render, get_list_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from rest_framework.response import Response
from rest_framework import generics

from posts.models import Post, PostView, Comment, Like
from posts.forms import PostForm, CommentForm
from posts.serializers import PostSerializer


class PostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect('detail', slug=post.slug)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })


    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)

        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)

        return object


class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
