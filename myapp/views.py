from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Nama


# 🔐 LOGIN
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


# 🔓 LOGOUT
def logout_user(request):
    logout(request)
    return redirect('/login/')


# 🔒 HOME (WAJIB LOGIN)
@login_required(login_url='/login/')
def home(request):

    # ➕ TAMBAH DATA
    if request.method == 'POST':
        nama = request.POST.get('nama')
        if nama:
            Nama.objects.create(nama=nama)
        return redirect('/')

    # 🔍 SEARCH
    keyword = request.GET.get('search')

    if keyword:
        data = Nama.objects.filter(nama__icontains=keyword)
    else:
        data = Nama.objects.all()

    return render(request, 'index.html', {
        'data': data,
        'keyword': keyword
    })


# ✏️ EDIT
@login_required(login_url='/login/')
def edit(request, id):
    item = get_object_or_404(Nama, id=id)

    if request.method == 'POST':
        item.nama = request.POST.get('nama')
        item.save()
        return redirect('/')

    return render(request, 'edit.html', {'item': item})


# 🗑️ HAPUS
@login_required(login_url='/login/')
def hapus(request, id):
    item = get_object_or_404(Nama, id=id)
    item.delete()
    return redirect('/')