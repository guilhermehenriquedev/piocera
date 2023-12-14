# coding=utf-8
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from .views import (PasswordCreateConfirmView, UserLogin, login_cadastro,
                    registration, sign_up_cadastro, teste, ActivateUserView)
from website.views import CustomPasswordResetView
urlpatterns = [
    # path('editar/', edit_user, name='edit_user'),
    path('cadastro/', registration, name='registration'),
    # path('cadastrar/concluido/',
    #      TemplateView.as_view(template_name='profiles/create/registration_complete.html'),
    #      name='django_registration_complete'),
    # path('cadastrar/finalizado/',
    #      TemplateView.as_view(template_name='profiles/create/registration_closed.html'),
    #      name='registration_finished'),
    path('entrar/', UserLogin.as_view(), name='entrar'),
    path('sair/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('sign-up-cadastro/', sign_up_cadastro, name='sign-up-cadastro'),
    path('login-cadastro/', login_cadastro, name='login-cadastro'),
    # path('alterar/senha/',
    #      auth_views.PasswordChangeView.as_view(template_name='profiles/change/password_change_form.html'),
    #      name='password_change'),
    # path('alterar/senha/concluido/',
    #      auth_views.PasswordChangeDoneView.as_view(template_name='profiles/change/password_change_done.html'),
    #      name='password_change_done'),

    # Reset de senha
    path(
        'resetar/senha/',
        auth_views.PasswordResetView.as_view(
            template_name='pages/auth/reset/password_reset_form.html',
            email_template_name='pages/auth/reset/password_reset_email.txt',
            html_email_template_name='pages/auth/reset/password_reset_email.html'
        ),
        name='password_reset'
    ),
    path(
        'resetar/senha/confirmar/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
                template_name='pages/auth/reset/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path('resetar/senha/completo/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='pages/auth/reset/password_reset_complete.html'),
         name='password_reset_complete'),
    path('resetar/senha/feito/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='pages/auth/reset/password_reset_done.html'),
         name='password_reset_done'),

    path('criar/senha/confirmar/<uidb64>/<token>/',
         PasswordCreateConfirmView.as_view(), name='password_create_confirm'),
    path('confirmar-cadastro/<uidb64>/<token>/', ActivateUserView.as_view(),
         name='confirm_registration'),
    #

    path('teste/', teste, name='teste')
]
