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
    # path('change-password/', auth_views.PasswordChangeView.as_view(template_name='users/change-password.html'), name='change-password'),
    path('change-password', views.change_password, name='change-password'),


    # path('password_reset', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password-reset'),
    # path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    # path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password-reset', views.UserPasswordResetView.as_view(), name='password-reset'),
    path('password_reset_confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
]
