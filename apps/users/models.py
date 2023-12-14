import os

from autoslug.settings import slugify
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from financial.asaas_customer import create_client
from radical.utils.utils import on_transaction_commit


def get_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.nickname:
        name_file = instance.nickname[:60]
    else:
        name_file = instance.get_full_name()
    return os.path.normcase(
        os.path.join(
            'usuario',
            slugify(name_file) + '.' + ext))


class Allergy(models.Model):
    name = models.CharField('Alergia', max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'Alergia'
        verbose_name_plural = 'Alergias'

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    CHOICE_CLOTHING = [
        ("PPM", "PP Masculino"),
        ("PM", "P Masculino"),
        ("MM", "M Masculino"),
        ("GM", "G Masculino"),
        ("GGM", "GG Masculino"),
        ("XGM", "XG Masculino"),

        ("PPF", "PP Feminino"),
        ("PF", "P Feminino"),
        ("MF", "M Feminino"),
        ("GF", "G Feminino"),
        ("GGF", "GG Feminino"),
        ("XGF", "XG Feminino"),
    ]

    CHOICE_BLOOD_TYPE = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    nickname = models.CharField('Apelido', max_length=150, null=True, blank=True)
    rg = models.CharField('RG', max_length=20, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=15, null=True, blank=True, unique=True)
    organ_expedidor = models.CharField('Orgão Emissor', max_length=50, null=True, blank=True)
    clothing = models.CharField('Vestuário', max_length=3, choices=CHOICE_CLOTHING, null=True, blank=True)
    birthdate = models.DateField('Data de nascimento', null=True, blank=True)
    cep = models.CharField('CEP', max_length=10, null=True, blank=True)

    country = models.CharField('País', max_length=150, null=True, blank=True)
    uf = models.CharField('UF', max_length=150, null=True, blank=True)
    city = models.CharField('Cidade', max_length=150, null=True, blank=True)

    neighborhood = models.CharField('Bairro', max_length=100, null=True, blank=True)
    address = models.CharField('Endereço', max_length=300, null=True, blank=True)
    phone = models.CharField('Telefone', max_length=30, null=True, blank=True)

    # allergy = models.ManyToManyField(Allergy, verbose_name='Alergia', blank=True)
    allergy = models.CharField('Alergia', max_length=500, null=True, blank=True)
    federation = models.ForeignKey("competition.Federation", on_delete=models.CASCADE,
                                   verbose_name='Federação afiliado', null=True, blank=True)

    name_emergency_contact = models.CharField('Nome de contato emergencial', max_length=150, null=True, blank=True)
    emergency_phone = models.CharField('Número de contato emergencial', max_length=30, null=True, blank=True)
    blood_type = models.CharField('Tipo sanguineo', max_length=3, choices=CHOICE_BLOOD_TYPE, null=True, blank=True)
    national_license = models.CharField('Licença Nacional CBA', max_length=150, null=True, blank=True)
    health_insurance_plan = models.CharField('Plano de saúde', max_length=150, null=True, blank=True)
    cnh = models.CharField('CNH', max_length=150, null=True, blank=True, unique=True)
    lgpd_acceptance = models.BooleanField('Aceite LGPD', default=False)

    profile_foto = models.ImageField(verbose_name='Foto de perfil', upload_to=get_path, max_length=100, null=True,
                                     blank=True)
    customer = models.CharField(verbose_name="Id Asaas", null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    @property
    def full_name(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
        indexes = [
            models.Index(
                name='index_users',
                fields=['is_active'],
            )
        ]

    def save(self, *args, **kwargs):
        if self.email and self.email != self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """

        if self.first_name and self.last_name:
            full_name = '{} {}'.format(self.first_name, self.last_name)
        else:
            full_name = '{}'.format(self.username)

        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        if self.first_name and self.last_name:
            short_name = '{}'.format(self.first_name)
        else:
            short_name = '{}'.format(self.username)
        return short_name.strip()

    def __str__(self):
        return self.get_full_name()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()


@receiver(post_save, sender=User)
def create_customer_user(sender, instance, **kwargs):
    try:
        if instance.customer is None or instance.customer == '':
            response = create_client(instance)
            instance.update(customer=response.get('id', False))
    except:
        pass
