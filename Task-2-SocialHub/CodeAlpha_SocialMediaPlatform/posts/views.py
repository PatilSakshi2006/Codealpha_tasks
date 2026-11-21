from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CommentForm, PostForm
from .models import Comment, Like, Post

def feed(request):
    posts = Post.objects.select_related("author").prefetch_related("likes", "comments__author")
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True))
    return render(request, "posts/feed.html", {"posts": posts, "liked_ids": liked_ids, "comment_form": CommentForm()})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been published.")
            return redirect("feed")
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form, "heading": "Create a post"})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect("feed")
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form, "heading": "Edit your post"})

@login_required
@require_POST
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect("feed")

@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    else:
        messages.error(request, "Please enter a comment before submitting.")
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    comment.delete()
    return redirect(request.POST.get("next") or "feed")
