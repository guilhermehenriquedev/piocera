from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

from .forms import UserChangeForm, UserCreationFormAdmin
from .models import User, Allergy


@admin.register(Allergy)
class AdminAllergy(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(User)
class AdminUser(auth_admin.UserAdmin):
    list_display = ['date_joined', 'profile_foto_thumbnail', 'username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active',
                    'last_login']
    form = UserChangeForm
    add_form = UserCreationFormAdmin
    model = User
    ordering = ['-date_joined']
    date_hierarchy = 'date_joined'
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (("Dados adicionais"), {
            "fields": (
                'customer', 'nickname', 'organ_expedidor', 'rg', 'cpf', 'clothing', 'birthdate',
                'cep', 'country', 'uf',
                'city', 'neighborhood',
                'address', 'phone', 'allergy', 'federation', 'name_emergency_contact', 'blood_type',
                'national_license', 'health_insurance_plan', 'cnh', 'lgpd_acceptance', 'profile_foto',)
        })
    )

    # noinspection DjangoSafeString
    def profile_foto_thumbnail(self, instance):
        try:
            thumbnailer = get_thumbnailer(instance.profile_foto)

            return mark_safe("<img src='{}{}' width='120' />".format(settings.MEDIA_URL,
                                                                     thumbnailer.get_thumbnail({'size': (120, 0)})))
        except OSError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Sem+Imagem' width='120' height='80'/>")

        except InvalidImageFormatError:
            return mark_safe("<img src='http://placehold.it/100x80&text=Imagem+Invalida' width='120' height='80'/>")

    profile_foto_thumbnail.short_description = "Foto de perfil"
