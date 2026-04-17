from django.contrib import admin
from django.urls import path
from myapp.views import home, hapus, edit, login_user, logout_user

urlpatterns = [
    # 🔧 ADMIN
    path('admin/', admin.site.urls),

    # 🏠 HOME
    path('', home, name='home'),

    # ✏️ EDIT
    path('edit/<int:id>/', edit, name='edit'),

    # 🗑️ HAPUS
    path('hapus/<int:id>/', hapus, name='hapus'),

    # 🔐 LOGIN
    path('login/', login_user, name='login'),

    # 🔓 LOGOUT
    path('logout/', logout_user, name='logout'),
]