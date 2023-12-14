import datetime

from django.db import models


class WebSite(models.Model):
    event_start_date = models.DateField('Data de Início do evento', null=True, blank=True)
    number_of_participants = models.PositiveIntegerField('Quantidade de participantes até hoje',
                                                         help_text='Colocar apenas número sem o milhar. Ex: 15 se for 15 mil.',
                                                         null=True, blank=True)
    number_of_states = models.PositiveIntegerField('Quantidade de estados',
                                                   help_text='Coloque a quantidade de estados que participaram no período do evento.',
                                                   null=True, blank=True)
    number_of_countries = models.PositiveIntegerField('Quantidade de países',
                                                      help_text='Coloque a quantidade de países que participaram no período do evento.',
                                                      null=True, blank=True)
    facebook_url = models.URLField('URL do Facebook', max_length=300, null=True, blank=True)
    instagram_url = models.URLField('URL do Instagram', max_length=300, null=True, blank=True)
    youtube_url = models.URLField('URL do YouTube', max_length=300, null=True, blank=True)
    whatsapp_url = models.URLField('URL do Whatsapp', max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configurações do Site'

    def __str__(self):
        return "WebSite settings"

    @property
    def history_years(self):
        diff = datetime.date.today() - self.event_start_date
        years = diff.days // 365
        return years


class Questions(models.Model):
    title = models.CharField('Título', max_length=300, null=True, blank=True)
    answer = models.TextField('Resposta', null=True, blank=True)
    is_active = models.BooleanField('Ativa?', help_text='Se ativa aparecerá no site', default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'Questão do FAQ'
        verbose_name_plural = 'Questões do FAQ'

    def __str__(self):
        return self.title


class Champion(models.Model):
    edition = models.PositiveIntegerField('Edição')
    modality = models.CharField('Modalidade', max_length=100)
    category = models.CharField('Categoria', max_length=100)
    name = models.CharField('Nome do Competidor', max_length=100)
    sponsorship = models.CharField('Patrocinador', max_length=500, null=True, blank=True)
    state = models.CharField('Estado', max_length=50)
    vehicle = models.CharField('Veículo', max_length=100)

    class Meta:
        verbose_name = 'Campeão'
        verbose_name_plural = 'Campeões'

    def save(self, *args, **kwargs):
        self.modality = self.modality.upper()
        super(Champion, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.modality} - {self.category} - {self.name}"


class Newsletter(models.Model):
    email = models.EmailField('E-mail')
    interest_area = models.CharField('Área de Interesse', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Data de atualização')

    class Meta:
        verbose_name = 'E-mail para Newsletter'
        verbose_name_plural = 'E-mails para Newsletter'

    def __str__(self):
        return self.email
