import os
from django.core.exceptions import ValidationError
from autoslug import AutoSlugField
from autoslug.settings import slugify
from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from radical.utils.utils import CHOICE_EDITION_STATUS
from django.utils import timezone
from competitor.models import Document


def get_path_sponsor_banner(instance, filename):
    ext = filename.split('.')[-1]
    if instance.name:
        rename = instance.name
    else:
        rename = instance.get_type_display

    return os.path.normcase(
        os.path.join(
            'patrocinador',
            'banner',
            slugify(rename[:60]) + '.' + ext))


def get_path_sponsor_logo(instance, filename):
    ext = filename.split('.')[-1]
    if instance.name:
        rename = instance.name
    else:
        rename = instance.get_type_display

    return os.path.normcase(
        os.path.join(
            'patrocinador',
            'logo',
            slugify(rename[:60]) + '.' + ext))


def get_path_banner(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'anuncio',
            'banner',
            slugify(instance.get_position_display()[:60]) + '.' + ext))


def get_path_modality_competition(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'modalidade',
            'competicao',
            slugify(instance.modality.name[:60]) + '.' + ext))


class Federation(models.Model):
    name = models.CharField('Nome', max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'Federação'
        verbose_name_plural = 'Federações'

    def __str__(self) -> str:
        return self.name


class Edition(models.Model):
    CHOICE_EDITION_TYPE = [
        (1, 'CERAPIO'),
        (2, 'PIOCERA'),
    ]

    ano = models.CharField('Ano', max_length=4)
    type = models.PositiveIntegerField('Tipo', choices=CHOICE_EDITION_TYPE, default=1)
    edition_date = models.DateTimeField('Data de lançamento')
    event_start_date = models.DateTimeField('Data inicial do evento', null=True)
    event_end_date = models.DateTimeField('Data final do evento', null=True)
    registration_start_date = models.DateTimeField('Data inicial para inscrição')
    registration_end_date = models.DateTimeField('Data final para inscrição')
    about = models.TextField('Sobre')
    status = models.PositiveIntegerField('Status', choices=CHOICE_EDITION_STATUS, default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')
    term = RichTextUploadingField(config_name='basic', verbose_name='Termo de responsabilidade', null=True, blank=True)
    check_list = models.OneToOneField('competitor.CheckList', on_delete=models.CASCADE, verbose_name='Check List',
                                      null=True, blank=True)

    class Meta:
        verbose_name = 'Edição'
        verbose_name_plural = 'Edições'

    def __str__(self) -> str:
        return self.ano

    def clone(self):
        new_edition = Edition.objects.create(
            ano=self.ano,
            type=self.type,
            edition_date=self.edition_date,
            registration_start_date=self.registration_start_date,
            registration_end_date=self.registration_end_date,
            about=self.about,
            status=self.status,
        )
        return new_edition


class Sponsor(models.Model):
    CHOICE_SPONSOR = [
        (1, 'PATROCINADOR'),
        (2, 'CO-PATROCINADOR'),
        (3, 'APOIO'),
    ]

    name = models.CharField('Nome do patrocinador', max_length=150, null=True, blank=True)
    type = models.PositiveIntegerField('Tipo', choices=CHOICE_SPONSOR, null=True, blank=True)
    logo = models.ImageField(upload_to=get_path_sponsor_logo, max_length=100)
    banner = models.ImageField(upload_to=get_path_sponsor_banner, max_length=100, null=True, blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, verbose_name="Edição")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Patrocinador'
        verbose_name_plural = 'Patrocinadores'

    def __str__(self) -> str:
        return self.name


class Banner(models.Model):
    CHOICE_BANNER_POSITION = [
        (1, 'BANNER PRICIPAL (1741x743)'),
        (2, 'BANNER TEXTO (1440x121)'),
        (3, 'BANNER OPÇÕES DE ESPORTES (4 banners - 288x124)'),
        (4, 'BACKGROUND DADOS'),
        (5, 'BACKGROUND EXPERIÊNCIA (1443x1140)'),
        (6, 'BACKGROUND AÇÕES (1443x1140)'),
        (7, 'BACKGROUND PERGUNTAS (1443x1140)'),
        (8, 'AREA COMPETIDOR (261 x 1077)')
    ]

    position = models.PositiveIntegerField('Posição', choices=CHOICE_BANNER_POSITION, null=True, blank=True)
    banner = models.ImageField('Banner', upload_to=get_path_banner, max_length=100)
    title = models.CharField(verbose_name='Titulo', null=True, help_text='Texto para opção de banner de esporte.',
                             max_length=20)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, verbose_name="Edição")

    order = models.PositiveIntegerField(verbose_name='Ordem', default=0)
    start_date = models.DateField(verbose_name='Data de início', default=timezone.now)
    end_date = models.DateField(verbose_name='Data de término', default=timezone.now)
    is_active = models.BooleanField(verbose_name='Ativo', default=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Banner e background'
        verbose_name_plural = 'Banners e backgrounds'

    def __str__(self) -> str:
        return 'banner - Posição {}'.format(self.get_position_display())


class WebSiteEdition(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, verbose_name="Edição")
    number_participants_previous_year = models.PositiveIntegerField('Quantidade de participantes no ano anterior',
                                                                    help_text='Colocar apenas número sem o milhar. Ex: '
                                                                              '15 se for 15 mil.', null=True,
                                                                    blank=True)
    number_km_previous_year = models.PositiveIntegerField('Quantidade de km ano anterior', null=True, blank=True)
    number_days_previous_year = models.PositiveIntegerField('Quantidade de dias no ano anterior', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Configuração da Edição'
        verbose_name_plural = 'Configurações das Edições'

    def __str__(self) -> str:
        return self.edition.ano


class CompetitionModality(models.Model):
    name = models.CharField('Nome', max_length=200)
    is_apoio_zequinha = models.BooleanField(verbose_name='Zequinha/Apoio', default=False,
                                            help_text='Marque a opção se for referente ao cadastro desse tipo pois irá '
                                                      'aparecer um formulário exclusivo.')
    slug = AutoSlugField(verbose_name='Link', populate_from='name', unique=True, max_length=150, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Modalidade'
        verbose_name_plural = 'Modalidades'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CompetitionModality, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class ModalityEdition(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, verbose_name="Edição")
    modality = models.ForeignKey(CompetitionModality, on_delete=models.CASCADE, verbose_name="Modalidade")
    description = models.CharField('Descrição', max_length=200)
    foto = models.ImageField(upload_to=get_path_modality_competition, height_field=None, width_field=None,
                             max_length=100)
    position = models.PositiveIntegerField("Ordem / Posição", default=0,
                                           help_text='Irá ser usado para ordenação nas telas necessárias')
    type_competitors = models.ManyToManyField('competitor.TypeCompetitor', verbose_name='Tipo de competidores',
                                              help_text='Adicione aqui os tipos de competidores que serão necessários na inscrição nessa modalidade'
                                              )
    documents = models.ManyToManyField(Document, verbose_name='Documentos')
    whatsapp_group = models.CharField('Link do grupo do whatsapp', max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Modalidade da Edição'
        verbose_name_plural = 'Modalidades das Edições'

    def __str__(self) -> str:
        return 'Modalidade {} da edição {}'.format(self.modality.name, self.edition.ano)

    def get_absolute_url(self):
        return reverse('modality', kwargs={'ano': self.edition.ano})

    def clone(self, new_edition):
        new_modality_edition = ModalityEdition.objects.create(
            edition=new_edition,
            modality=self.modality,
            description=self.description,
            foto=self.foto,
        )
        new_modality_edition.type_competitors.set(self.type_competitors.all())
        return new_modality_edition


class CompetitionCategory(models.Model):
    name = models.CharField('Nome', max_length=200)
    slug = AutoSlugField(verbose_name='Link', populate_from='name', unique=True, max_length=150, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CompetitionCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class CategoryModality(models.Model):
    category = models.ForeignKey(CompetitionCategory, on_delete=models.CASCADE, verbose_name="Categoria")
    modality_edition = models.ForeignKey(ModalityEdition, on_delete=models.CASCADE, verbose_name="Modalidade",
                                         null=True)
    order = models.IntegerField('Ordem', null='True', blank="True")
    number_vacancies = models.IntegerField('Quantidade de vagas', null=True, blank=True)
    has_age = models.BooleanField('Tem faixa etária', default=False)
    min_age = models.PositiveIntegerField('Idade mínima', null=True, blank=True)
    max_age = models.PositiveIntegerField('Idade máxima', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Categoria da Modalidade'
        verbose_name_plural = 'Categorias das Modalidades'
        ordering = ("order",)

    def __str__(self) -> str:
        return '{} - {}'.format(self.category.name, self.modality_edition.modality.name)

    def clone(self, new_modality_edition):
        new_category_modality = CategoryModality.objects.create(
            category=self.category,
            modality_edition=new_modality_edition,
            number_vacancies=self.number_vacancies,
        )
        return new_category_modality
