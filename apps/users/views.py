from django.conf import settings
from django.contrib import messages
# from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import (REDIRECT_FIELD_NAME)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import auth_login, PasswordResetConfirmView, \
    LoginView
from .forms import AuthenticationCaptchaForm, UserCreationForm, \
    UserProfileComplementForm
from django.contrib.auth import login, authenticate
from .send_email import CreatePasswordView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from users.models import User

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Conta criada para {username}!')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                if request.GET.get('next'):
                    next_url = request.GET.get('next')
                    return redirect(next_url)
                else:
                    return redirect('/')
            else:
                messages.error(request, 'Email ou senha inválidos.')
        else:
            messages.error(request, 'Dados inválidos.')
    else:
        form = UserCreationForm()
    return render(request, 'pages/auth/create-account.html', {'form': form})


class UserLogin(LoginView):
    template_name = 'pages/auth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'next': self.request.GET.get('next')})
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)

            if 'next' in self.request.GET:
                return redirect(self.request.GET['next'])
            else:
                return redirect(reverse('home'))

    def form_invalid(self, form):
        messages.error(self.request, 'Email ou senha inválidos.')
        return self.render_to_response(self.get_context_data(form=form))

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('home'))
        else:
            context = super(UserLogin, self).render_to_response(context, **response_kwargs)
            return context


class PasswordCreateConfirmView(PasswordResetConfirmView):
    """
    Essa função é pra criação de senha e ativação de usuario após ser feito o cadastro sem senha - pode servir para o copiloto
    """
    form_class = UserProfileComplementForm
    reset_url_token = 'set-password'
    success_url = reverse_lazy('registration_finished')
    template_name = 'pages/auth/create/complement_activate_user.html'

    def form_valid(self, form):
        user = form.save()
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super(PasswordCreateConfirmView, self).form_valid(form)


class ActivateUserView(PasswordResetConfirmView):
    # form_class = UserActiveForm
    reset_url_token = 'set-password'
    success_url = reverse_lazy('registration_finished')
    template_name = 'profiles/create/activate_user.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        if self.validlink:
            context['validlink'] = True
            # activate
            User.objects.filter(email=self.user).update(is_active=True)
        else:
            context.update({
                'validlink': False,
            })
            try:
                if not self.user.is_active:
                    CreatePasswordView().email_envio(from_user_email=self.user.email,
                                                     is_active=False,
                                                     email_template_name='pages/auth/create/password_created_email.txt',
                                                     html_email_template_name='pages/auth/create/password_created_email.html',
                                                     subject_template_name='pages/auth/create/password_created_subject.txt')
            except:
                pass

        return context


def sign_up_cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            messages.success(request, f'Conta criada para {username}!')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
        else:
            # form = UserCreationForm()
            if 'next' in request.GET:
                return redirect(request.GET['next'])

    return JsonResponse({'criado': 'true', 'logado': 'true'}, safe=False)


def login_cadastro(request):
    if request.method == 'POST':
        form = AuthenticationCaptchaForm(data=request.POST)

        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
            else:
                messages.error(request, 'Usuário ou senha inválidos')
        else:
            form = AuthenticationCaptchaForm()
    return HttpResponse()


def teste(request):
    email = 'raifranlucas@outlook.com'
    CreatePasswordView().email_envio(from_user_email=email,
                                     email_template_name='pages/auth/create/password_created_email.txt',
                                     html_email_template_name='pages/auth/create/password_created_email.html',
                                     subject_template_name='pages/auth/create/password_created_subject.txt')
    return HttpResponse('sahdsah')
