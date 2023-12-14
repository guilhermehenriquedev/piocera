# coding=utf-8

from django.conf import settings
from django.contrib.auth.forms import _unicode_ci_compare
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


UserModel = get_user_model()

class CreatePasswordView():
    email_template_name = 'registration/password_created_email.html'
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_created_subject.txt'
    token_generator = default_token_generator

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
        })

        return (
            u for u in active_users
            if u.has_usable_password() and
               _unicode_ci_compare(email, getattr(u, email_field_name))
        )


    def email_envio(self, domain_override=None,
             subject_template_name=subject_template_name,
             email_template_name=email_template_name,
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None, from_user_email=None, is_import=False, is_user=True,
             context_email=None, from_users_emails=None):

        email = from_user_email
        email_field_name = UserModel.get_email_field_name()

        schema = 'https://'
        if settings.DEBUG == True:
            schema = 'http://'

        site = get_current_site(request)

        context = {
            'domain': schema + site.domain,
            'site_name': site.name,
        }

        if is_user:
            for user in self.get_users(email):
                user_email = getattr(user, email_field_name)
                context.update({
                    'is_import': is_import,
                    'email': user_email,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': token_generator.make_token(user),
                    'protocol': 'https' if use_https else 'http',
                    **(extra_email_context or {}),
                })
                self.send_mail(
                    subject_template_name, email_template_name, context, from_email,
                    user_email, html_email_template_name=html_email_template_name
                )
        else:
            user_email = from_users_emails
            for email in user_email:
                context.update({
                    'email': email,
                    'context': context_email,
                })
                # print('enviado: ', email)
                self.send_mail(
                    subject_template_name, email_template_name, context, from_email,
                    email, html_email_template_name=html_email_template_name,
                )
                # print('ok')

