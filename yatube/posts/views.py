from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from .models import Post, Group, User
from .forms import PostForm
from yatube.constants import POSTS_PER_STR


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_PER_STR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, POSTS_PER_STR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__exact=user)
    posts_count = Post.objects.filter(author__exact=user).count
    paginator = Paginator(posts, POSTS_PER_STR)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "username": username,
        "author": user,
        "posts_count": posts_count,
        "page_obj": page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_count = Post.objects.filter(author__exact=post.author).count
    context = {
        "post": post,
        "posts_count": posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    context = {
        'title': 'Добавить запись',
        'submit_btn': 'Сохранить',
        'form': form,
    }
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('posts:profile', request.user)
        return render(request, "posts/create_post.html", context)
    return render(request, "posts/create_post.html", context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post.id)
    form = PostForm(request.POST or None)
    context = {
        'title': 'Редактировать пост',
        'submit_btn': 'Добавить',
        'is_edit': True,
        'form': form,
    }
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('posts:post_detail', post.pk)
        return render(request, "posts/create_post.html", context)
    return render(request, "posts/create_post.html", context)
