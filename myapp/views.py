from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Profile, Follow


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username sudah dipakai'
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(user=user)

        return redirect('login')

    return render(request, 'register.html')


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Username / Password salah'
        })

    return render(request, 'login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# HOME
# =========================
@login_required
def home(request):
    posts = Post.objects.all().order_by('-id')

    return render(request, 'home.html', {
        'posts': posts
    })


# =========================
# UPLOAD POSTINGAN
# =========================
@login_required
def upload_post(request):
    if request.method == "POST":
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if image:
            Post.objects.create(
                user=request.user,
                caption=caption,
                image=image
            )

    return redirect('home')


# =========================
# LIKE POST
# =========================
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('home')


# =========================
# HAPUS POST
# =========================
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:
        post.delete()

    return redirect('home')


# =========================
# EDIT POST
# =========================
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return redirect('home')

    if request.method == "POST":
        caption = request.POST.get('caption')
        post.caption = caption
        post.save()

        return redirect('home')

    return render(request, 'edit.html', {
        'post': post
    })


# =========================
# KOMENTAR
# =========================
@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text')

        if text:
            Comment.objects.create(
                user=request.user,
                post=post,
                text=text
            )

    return redirect('home')


# =========================
# PROFILE USER
# =========================
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    my_posts = Post.objects.filter(
        user=request.user
    ).order_by('-id')

    followers = Follow.objects.filter(
        following=request.user
    ).count()

    following = Follow.objects.filter(
        follower=request.user
    ).count()

    return render(request, 'profile.html', {
        'profile': profile,
        'posts': my_posts,
        'followers': followers,
        'following': following
    })


# =========================
# UPDATE PROFILE
# =========================
@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        photo = request.FILES.get('photo')
        bio = request.POST.get('bio')

        if photo:
            profile.photo = photo

        profile.bio = bio
        profile.save()

    return redirect('profile')


# =========================
# FOLLOW USER
# =========================
@login_required
def follow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if request.user != target:
        Follow.objects.get_or_create(
            follower=request.user,
            following=target
        )

    return redirect('home')


# =========================
# UNFOLLOW USER
# =========================
@login_required
def unfollow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)

    Follow.objects.filter(
        follower=request.user,
        following=target
    ).delete()

    return redirect('home')