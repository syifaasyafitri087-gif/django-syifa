from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .models import (
    Post,
    Comment,
    Profile,
    Follow,
    Story,
    Message
)


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

        Profile.objects.create(
            user=user,
            is_online=False,
            last_seen=timezone.now()
        )

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

        if user:

            login(request, user)

            profile, created = Profile.objects.get_or_create(
                user=user
            )

            profile.is_online = True
            profile.last_seen = timezone.now()
            profile.save()

            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Login gagal'
        })

    return render(request, 'login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):

    if request.user.is_authenticated:

        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

        profile.is_online = False
        profile.last_seen = timezone.now()
        profile.save()

    logout(request)

    return redirect('login')


# =========================
# HOME
# =========================
@login_required
def home(request):

    profile = request.user.profile
    profile.is_online = True
    profile.last_seen = timezone.now()
    profile.save()

    posts = Post.objects.all().order_by('-id')

    stories = Story.objects.filter(
        expires_at__gt=timezone.now()
    ).order_by('-id')

    return render(request, 'home.html', {
        'posts': posts,
        'stories': stories
    })


# =========================
# EXPLORE
# =========================
@login_required
def explore_view(request):
    posts = Post.objects.all().order_by('-id')

    return render(request, 'explore.html', {
        'posts': posts
    })


# =========================
# REELS
# =========================
@login_required
def reels_view(request):
    posts = Post.objects.exclude(
        video=''
    ).exclude(
        video=None
    ).order_by('-id')

    return render(request, 'reels.html', {
        'posts': posts
    })


# =========================
# CHAT
# =========================
@login_required
def chat_view(request, user_id=None):

    request.user.profile.is_online = True
    request.user.profile.last_seen = timezone.now()
    request.user.profile.save()

    users = User.objects.exclude(id=request.user.id)

    selected_user = None
    messages = []

    if user_id:

        selected_user = get_object_or_404(
            User,
            id=user_id
        )

        messages = Message.objects.filter(
            Q(sender=request.user, receiver=selected_user) |
            Q(sender=selected_user, receiver=request.user)
        ).order_by('created_at')

        Message.objects.filter(
            sender=selected_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

    return render(request, 'chat.html', {
        'users': users,
        'selected_user': selected_user,
        'messages': messages
    })


# =========================
# SEND MESSAGE
# =========================
@login_required
def send_message(request, user_id):

    if request.method == "POST":

        receiver = get_object_or_404(
            User,
            id=user_id
        )

        text = request.POST.get('text')

        if text:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                text=text,
                delivered=True
            )

    return redirect(f'/chat/{user_id}/')


# =========================
# UPLOAD POST
# =========================
@login_required
def upload_post(request):

    if request.method == "POST":

        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        Post.objects.create(
            user=request.user,
            caption=caption,
            image=image,
            video=video
        )

    return redirect('home')


# =========================
# UPLOAD STORY
# =========================
@login_required
def upload_story(request):

    if request.method == "POST":

        image = request.FILES.get('image')

        if image:
            Story.objects.create(
                user=request.user,
                image=image
            )

    return redirect('home')


# =========================
# LIKE
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
# DELETE POST
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
        post.caption = request.POST.get('caption')
        post.save()

        return redirect('home')

    return render(request, 'edit.html', {
        'post': post
    })


# =========================
# COMMENT
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
# PROFILE
# =========================
@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    posts = Post.objects.filter(
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
        'posts': posts,
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
# FOLLOW
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
# UNFOLLOW
# =========================
@login_required
def unfollow_user(request, user_id):

    target = get_object_or_404(User, id=user_id)

    Follow.objects.filter(
        follower=request.user,
        following=target
    ).delete()

    return redirect('home')