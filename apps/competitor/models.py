import os
import random
import string
import uuid
from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.db import models
from cloudinary.models import CloudinaryField


def get_path_model_documentation(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'documentacao',
            'modelo',
            slugify(instance.title[:60]) + '.' + ext))


def get_path_documentation(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'documentacao',
            'modelo',
            slugify(instance.user.first_name[:60]) + '.' + ext))


def get_registration_number():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    allowed_chars = list(letters + numbers)
    code = "".join([random.choice(allowed_chars) for _ in range(12)])
    while Registration.objects.filter(registration_number=code).exists():
        code = "".join([random.choice(allowed_chars) for _ in range(12)])
    return code


class TeamMembers(models.Model):
    MEMBER_POSITION_CHOICES = (
        (1, 'Chefe'),
        (2, 'Membro'),
        (3, 'Zequinha'),
        (4, 'Apoio'),
    )
    team = models.ForeignKey('competitor.Team', on_delete=models.CASCADE, verbose_name='Equipe')
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name='Membro')
    member_position = models.PositiveIntegerField('Posição do membro', help_text='O que você é na equipe?',
                                                  choices=MEMBER_POSITION_CHOICES, null=True)

    class Meta:
        verbose_name = 'Integrante da Equipe'
        verbose_name_plural = 'Integrantes das Equipes'

    def __str__(self) -> str:
        return self.team.name


class Team(models.Model):
    coordinator = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name='Coordenador')
    name = models.CharField('Nome', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'

    def __str__(self) -> str:
        return self.name


class VehicleBrand(models.Model):
    name = models.CharField('Nome', max_length=50)

    class Meta:
        verbose_name = 'Marca de veículo'
        verbose_name_plural = 'Marcas de veículos'

    def __str__(self) -> str:
        return self.name


class VehicleModel(models.Model):
    name = models.CharField('Nome', max_length=50)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, verbose_name='Marca')

    class Meta:
        verbose_name = 'Modelo de veículo'
        verbose_name_plural = 'Modelos de veículos'

    def __str__(self) -> str:
        return self.name


class TireBrand(models.Model):
    name = models.CharField('Nome', max_length=50)

    class Meta:
        verbose_name = 'Marca de pneu'
        verbose_name_plural = 'Marcas de pneus'

    def __str__(self) -> str:
        return self.name


class Registration(models.Model):
    CHOICE_STATUS = [
        ('1', 'Registro'),
        ('2', 'Pago'),
        ('3', 'Homologado'),
        ('4', 'Cancelado'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Equipe', blank=True, null=True)
    # Todo: talvez não  precise desse campo ja que o campo que relaciona com equipe pode ser nulo
    has_team = models.BooleanField('Sem equipe', default=False)
    sponsorship = models.CharField('Patrocinador', max_length=250, blank=True, null=True)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name='Modelo do veículo',
                                      blank=True, null=True)
    vehicle_brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, verbose_name='Marca do veículo',
                                      blank=True, null=True)
    tire_brand = models.ForeignKey(TireBrand, on_delete=models.CASCADE, verbose_name='Marca do pneu',
                                   blank=True, null=True)
    wheel_rim = models.CharField('Aro da roda', max_length=50, blank=True, null=True)
    lot = models.ForeignKey("financial.Lot", on_delete=models.CASCADE, verbose_name='Lote')
    status = models.CharField(verbose_name='status', max_length=12, choices=CHOICE_STATUS, default='1')
    payment_status = models.BooleanField('Status de pagamento', default=False)
    registration_number = models.CharField('Número de inscrição', max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

    def __str__(self):
        return 'Inscrição n° {} ({})'.format(self.registration_number,
                                             self.lot.category_modality.modality_edition.edition.ano)

    def save(self, *args, **kwargs):
        if not self.registration_number:
            random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.registration_number = f"{random_chars}-{self.lot.category_modality.modality_edition.edition.ano}"

            while Registration.objects.filter(registration_number=self.registration_number).exists():
                random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                self.registration_number = f"{random_chars}-{self.lot.category_modality.modality_edition.edition.ano}"

        super().save(*args, **kwargs)


class CompetitorsRegistration(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, verbose_name='Inscrição')
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name='Usuário')
    type = models.ForeignKey('competitor.TypeCompetitor', verbose_name='Tipo', null=True, default=None,
                             on_delete=models.CASCADE)
    number = models.IntegerField('Número', blank=True, null=True)
    thermo = models.BooleanField('Aceite Termo', default=False)
    competitor_card = models.BooleanField('Geração do cartão do competidor', default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Inscrição do Competidor'
        verbose_name_plural = 'Inscrições do Competidor'

    def __str__(self):
        return f'Inscrição: {self.registration} - {self.user}'


class Boleto(models.Model):
    competitor_registration = models.ForeignKey(CompetitorsRegistration, on_delete=models.CASCADE,
                                                verbose_name='Inscrição do competidor', null=True, blank=True)
    document_file = CloudinaryField('Documentação', folder="boletos")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    def __str__(self):
        return f"Boleto - {self.competitor_registration.user.username}"


class CheckList(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nome', unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Checklist'
        verbose_name_plural = 'Checklists'

    def __str__(self) -> str:
        return self.name


class CheckListItem(models.Model):
    text = models.CharField(max_length=500, verbose_name='Texto')
    checklist = models.ForeignKey(CheckList, on_delete=models.CASCADE, verbose_name='Checklist')
    models_url = CloudinaryField('Modelo', folder="check_list_modelo", null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Checklist Item'
        verbose_name_plural = 'Checklists Items'

    def __str__(self):
        return f'Item da Checklist: {self.checklist} - {self.text}'


class CompetitorCheckList(models.Model):
    competitor_registration = models.ForeignKey(CompetitorsRegistration, on_delete=models.CASCADE,
                                                verbose_name='Inscrição do Competidor')
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, verbose_name='Checklist')

    check_list_item_concluded = models.ManyToManyField(CheckListItem, verbose_name='Itens concluídos', blank=True)

    class Meta:
        verbose_name = 'Checklist do Competidor'
        verbose_name_plural = 'Checklists dos Competidores'

    def __str__(self):
        return f'Checklists Items: {self.check_list} - {self.competitor_registration.user.full_name}'


class CompetitorCheckListItem(models.Model):
    competitor_checklist = models.ForeignKey(CompetitorCheckList, on_delete=models.CASCADE,
                                             verbose_name='Checklist do Competidor')
    check_list_item = models.ForeignKey(CheckListItem, on_delete=models.CASCADE, verbose_name='Item da Checklist')
    confirmation_image = CloudinaryField('Imagem de Confirmação',
                                         folder="competitor_checklist_images", null=True)

    class Meta:
        verbose_name = 'Item da Checklist do Competidor'
        verbose_name_plural = 'Itens das Checklists dos Competidores'


class TypeCompetitor(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nome', unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Tipo do Competidor'
        verbose_name_plural = 'Tipo dos Competidores'

    def __str__(self) -> str:
        return self.name


class Document(models.Model):
    title = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True, null=True, blank=True)
    model = models.FileField(upload_to=get_path_model_documentation, verbose_name='Modelo do Documento', null=True,
                             blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Modelo da Documentação'
        verbose_name_plural = 'Modelos das Documentações'

    def __str__(self) -> str:
        return self.title


class RegistrationDocuments(models.Model):
    CHOICE_APPROVAL_STATUS = [
        ('1', 'Inscrição'),
        ('2', 'Em análise'),
        ('3', 'Aprovado'),
        ('4', 'Negado'),
        ('5', 'Cancelado'),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE,
                             verbose_name='Usuário')
    competitor_registration = models.ForeignKey(CompetitorsRegistration, on_delete=models.CASCADE,
                                                verbose_name='Inscrição do competidor', null=True, blank=True)
    document_type = models.ForeignKey(Document, on_delete=models.CASCADE,
                                      verbose_name='Tipo de documento')
    document_file = models.FileField(upload_to=get_path_documentation,
                                     verbose_name='Documentação')
    approval_status = models.CharField("Status de aprovação", max_length=2,
                                       choices=CHOICE_APPROVAL_STATUS,
                                       default=1)
    approval_status_changed = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Documentação da Inscrição'
        verbose_name_plural = 'Documentações da inscrição'

    def __str__(self) -> str:
        return f'Documento:{self.document_type.title}, Competidor: {self.user.get_full_name()}-'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = RegistrationDocuments.objects.get(pk=self.pk)
            if orig.approval_status != self.approval_status:
                self.approval_status_changed = True
        super().save(*args, **kwargs)
