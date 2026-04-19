from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Nama, Post, Like, Comment, Profile


# ======================
# REGISTER
# ======================
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username sudah digunakan'
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')


# ======================
# LOGIN
# ======================
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

        return render(request, 'login.html', {
            'error': 'Username / Password salah'
        })

    return render(request, 'login.html')


# ======================
# LOGOUT
# ======================
def logout_user(request):
    logout(request)
    return redirect('/login/')


# ======================
# HOME
# ======================
@login_required(login_url='/login/')
def home(request):
    posts = Post.objects.all().order_by('-id')

    return render(request, 'index.html', {
        'posts': posts
    })


# ======================
# UPLOAD POST
# ======================
@login_required(login_url='/login/')
def upload_post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image')

        if caption or image:
            Post.objects.create(
                user=request.user,
                caption=caption,
                image=image
            )

    return redirect('/')


# ======================
# LIKE
# ======================
@login_required(login_url='/login/')
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    cek = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if cek:
        cek.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect('/')


# ======================
# COMMENT
# ======================
@login_required(login_url='/login/')
def comment_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        text = request.POST.get('text')

        if text:
            Comment.objects.create(
                user=request.user,
                post=post,
                text=text
            )

    return redirect('/')


# ======================
# DELETE POST
# ======================
@login_required(login_url='/login/')
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.user == request.user:
        post.delete()

    return redirect('/')


# ======================
# EDIT POST
# ======================
@login_required(login_url='/login/')
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.user != request.user:
        return redirect('/')

    if request.method == 'POST':
        caption = request.POST.get('caption')

        if caption:
            post.caption = caption
            post.save()

        return redirect('/')

    return render(request, 'edit_post.html', {
        'post': post
    })


# ======================
# PROFILE USER
# ======================
@login_required(login_url='/login/')
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        bio = request.POST.get('bio')
        foto = request.FILES.get('foto')

        profile.bio = bio

        if foto:
            profile.foto = foto

        profile.save()

        return redirect('/profile/')

    return render(request, 'profile.html', {
        'profile': profile
    })