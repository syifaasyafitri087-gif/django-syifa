from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from myapp import views


urlpatterns = [

    # =========================
    # ADMIN
    # =========================
    path('admin/', admin.site.urls),


    # =========================
    # AUTH
    # =========================
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),


    # =========================
    # HOME
    # =========================
    path('home/', views.home, name='home'),


    # =========================
    # PREMIUM PAGE
    # =========================
    path('explore/', views.explore_view, name='explore'),
    path('reels/', views.reels_view, name='reels'),

    # CHAT
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_room'),
    path('send-message/<int:user_id>/', views.send_message, name='send_message'),


    # =========================
    # POSTINGAN
    # =========================
    path('upload/', views.upload_post, name='upload'),
    path('story-upload/', views.upload_story, name='upload_story'),

    path('like/<int:post_id>/', views.like_post, name='like'),
    path('delete/<int:post_id>/', views.delete_post, name='delete'),
    path('edit/<int:post_id>/', views.edit_post, name='edit'),
    path('comment/<int:post_id>/', views.add_comment, name='comment'),


    # =========================
    # PROFILE
    # =========================
    path('profile/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),


    # =========================
    # FOLLOW
    # =========================
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),
]


# =========================
# MEDIA & STATIC
# =========================
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)