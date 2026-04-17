from django.shortcuts import render, redirect
from .models import Nama

# 🔐 AUTH
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# =========================
# 🏠 HOME (CRUD + SEARCH)
# =========================
@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')

        if nama:
            Nama.objects.create(
                nama=nama,
                user=request.user   # 🔥 data per user
            )

        return redirect('/')

    # 🔍 SEARCH
    keyword = request.GET.get('search')

    if keyword:
        data = Nama.objects.filter(
            user=request.user,
            nama__icontains=keyword
        )
    else:
        data = Nama.objects.filter(
            user=request.user
        )

    return render(request, 'index.html', {
        'data': data,
        'keyword': keyword
    })


# =========================
# 🗑️ HAPUS
# =========================
@login_required(login_url='/login/')
def hapus(request, id):
    data = Nama.objects.get(id=id, user=request.user)
    data.delete()
    return redirect('/')


# =========================
# ✏️ EDIT
# =========================
@login_required(login_url='/login/')
def edit(request, id):
    data = Nama.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        data.nama = request.POST.get('nama')
        data.save()
        return redirect('/')

    return render(request, 'edit.html', {'data': data})


# =========================
# 🔐 LOGIN
# =========================
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {
                'error': 'Username atau Password salah'
            })

    return render(request, 'login.html')


# =========================
# 🔓 LOGOUT
# =========================
def logout_user(request):
    logout(request)
    return redirect('/login/')


# =========================
# 📝 REGISTER
# =========================
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # cek username
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username sudah digunakan'
            })

        # buat user baru
        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')