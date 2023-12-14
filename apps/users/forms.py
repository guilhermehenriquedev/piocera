from captcha import widgets
from captcha.fields import ReCaptchaField
from django.conf import settings
from django import forms
from django.contrib.auth import forms as AuthForm
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from .models import User
from datetime import date
from django.forms.widgets import DateInput
from validate_docbr import CPF, CNH


class UserCustomForm(forms.ModelForm):
    pass


class UserChangeForm(AuthForm.UserChangeForm, UserCustomForm):
    class Meta(AuthForm.UserChangeForm.Meta):
        model = User


class UserCreationFormAdmin(AuthForm.UserCreationForm, UserCustomForm):
    class Meta(AuthForm.UserCreationForm.Meta):
        model = User
        fields = ['username', 'cpf', 'email', 'password1', 'password2']


class UserCreationForm(AuthForm.UserCreationForm, UserCustomForm):
    email = forms.CharField(label='email', required=False)
    birthdate = forms.DateField(label='birth_date', required=True, widget=DateInput(attrs={'type': 'date'}))
    lgpd_acceptance = forms.BooleanField(label='lgpd_acceptance', required=True)

    class Meta(AuthForm.UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'cpf', 'email',
                  'password1', 'password2', 'lgpd_acceptance']

    def clean_lgpd_acceptance(self):
        lgpd_acceptance = self.cleaned_data.get('lgpd_acceptance')

        if not lgpd_acceptance:
            raise forms.ValidationError('Você deve aceitar os termos para prosseguir.')

        return lgpd_acceptance

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            age = date.today().year - birthdate.year
            if age < 18:
                raise forms.ValidationError("Você deve ter 18 anos ou mais para se cadastrar.")
        return birthdate

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not CPF().validate(cpf):
            raise forms.ValidationError("CPF inválido")
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['username']
        user.birthdate = self.cleaned_data['birthdate']
        user.cpf = self.cleaned_data['cpf']
        user.lgpd_acceptance = self.cleaned_data['lgpd_acceptance']

        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


class AuthenticationCaptchaForm(AuthenticationForm):
    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=widgets.ReCaptchaV3(
            attrs={
                'data-theme': 'clean',
                'data-size': 'large',
            }), required=True)


class UserActiveForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'cpf']

    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=widgets.ReCaptchaV3(
            attrs={
                'data-theme': 'clean',
                'data-size': 'large',
            }), required=True)


class UserProfileComplementForm(SetPasswordForm):
    cpf = forms.CharField(label='cpf', required=True)
    terms_and_privacity = forms.BooleanField(label='terms_and_privacity', required=True)
    date_birth = forms.DateField(label='date_birth', required=True)

    if not settings.DEBUG:
        captcha = ReCaptchaField(widget=widgets.ReCaptchaV3(
            attrs={
                'data-theme': 'clean',
                'data-size': 'large',
            }), required=True)

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.is_active = True
        self.user.cpf = self.cleaned_data["cpf"]
        self.user.is_terms = self.cleaned_data["terms_and_privacity"]
        self.user.date_birth = self.cleaned_data["date_birth"]

        if commit:
            self.user.save()
        return self.user

    def clean_cpf(self):
        if self.cleaned_data['cpf']:
            if User.objects.filter(cpf__iexact=self.cleaned_data['cpf']):
                raise forms.ValidationError("Este CPF já está em uso. Por favor, preencha um CPF diferente.")
            return self.cleaned_data['cpf']
