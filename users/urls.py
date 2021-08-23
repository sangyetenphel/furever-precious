# from django.contrib.auth import views as auth_views
from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user-register'),
    path('profile/', views.user_profile, name='user-profile'),
    path('login', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('review_delete/<int:id>', views.user_review_delete, name='user-review-delete'),
    path('change-password', views.change_password, name='change-password'),
    # For resetting the password
    path('password-reset', views.UserPasswordResetView.as_view(), name='password-reset'),
    path('password_reset_confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
