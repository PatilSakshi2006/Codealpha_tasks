from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import ProfileForm, SignUpForm
from .models import Follow

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("feed")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to SocialHub! Your account is ready.")
            return redirect("feed")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def edit_profile(request):
    profile, _ = request.user.profile.__class__.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/edit_profile.html", {"form": form})

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = profile_user.profile.__class__.objects.get_or_create(user=profile_user)
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    user_posts = profile_user.posts.select_related("author").prefetch_related("likes", "comments").all()
    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "profile": profile,
        "user_posts": user_posts,
        "is_following": is_following,
        "followers_count": profile_user.follower_links.count(),
        "following_count": profile_user.following_links.count(),
    })

@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "You cannot follow yourself.")
    else:
        relation, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            relation.delete()
    return redirect("profile", username=username)

def search_users(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id if request.user.is_authenticated else None)[:25] if query else User.objects.none()
    return render(request, "accounts/search.html", {"query": query, "users": users})
