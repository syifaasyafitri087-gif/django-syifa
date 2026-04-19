from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from myapp.views import (
    home,
    login_user,
    logout_user,
    register_user,
    upload_post,
    like_post,
    comment_post,
    delete_post,
    edit_post,
    profile
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),

    path('upload/', upload_post, name='upload'),

    path('like/<int:id>/', like_post, name='like'),
    path('comment/<int:id>/', comment_post, name='comment'),

    path('delete/<int:id>/', delete_post, name='delete'),
    path('edit/<int:id>/', edit_post, name='edit'),

    # 🔥 PROFILE
    path('profile/', profile, name='profile'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)