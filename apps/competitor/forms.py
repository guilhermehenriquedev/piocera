from users.models import User, Allergy
from django import forms
from .models import Registration, Team, CompetitorsRegistration, \
    TypeCompetitor, RegistrationDocuments, VehicleBrand, VehicleModel, TireBrand
from financial.models import Lot
from competition.models import Federation
from django.contrib.admin.widgets import FilteredSelectMultiple
from validate_docbr import CPF, CNH

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

TYPE_CHOICE = (
    (1, 'Piloto'),
    (2, 'Co-Piloto'),
    (3, 'Zequinha')
)

MEMBER_POSITION_CHOICES = (
    (1, 'Chefe'),
    (2, 'Membro'),
    (3, 'Zequinha'),
    (4, 'Apoio'),
)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('coordinator', 'name')


class RegistrationForm(forms.ModelForm):
    create_team = forms.BooleanField(label='Criar nova equipe?', required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
    lot = forms.ModelChoiceField(queryset=Lot.objects.all(), required=False)
    sponsorship = forms.CharField(label='Patrocinador', required=False, max_length=250)
    vehicle_brand = forms.ModelChoiceField(
        queryset=VehicleBrand.objects.all(),
        required=False,
        widget=forms.Select(attrs={'id': 'vehicle-brand'})
    )
    vehicle_model = forms.ModelChoiceField(
        queryset=VehicleModel.objects.all(),
        required=False,
        widget=forms.Select(attrs={'id': 'vehicle-model'})
    )
    tire_brand = forms.ModelChoiceField(queryset=TireBrand.objects.all(), required=False)
    registration_number = forms.CharField(label='registration_number', required=False, max_length=12)
    wheel_rim = forms.CharField(label='Aro da roda', required=False, max_length=10)
    create_team_name = forms.CharField(label='Nome da equipe', required=False, max_length=150)
    team_member = forms.ChoiceField(label='O que você é da equipe?', required=False, choices=MEMBER_POSITION_CHOICES)

    class Meta:
        model = Registration
        exclude = ('status',)


# Cadastro para o competidor, vai haver tipo (piloto, copiloto .....)
class CompetitorRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(label='Nome Completo', required=True, max_length=150)
    registration = forms.ModelChoiceField(queryset=Registration.objects.all(), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    nickname = forms.CharField(label='Apelido', required=False, max_length=150)
    cpf = forms.CharField(label='CPF', required=True, max_length=15)
    rg = forms.CharField(label='RG', required=True, max_length=20)
    organ_expedidor = forms.CharField(label='Orgão Emissor', required=True, max_length=50)
    clothing = forms.ChoiceField(label='Vestuário', required=False, choices=CHOICE_CLOTHING)
    birthdate = forms.DateField(label='Data de nascimento', required=True)
    cep = forms.CharField(label='CEP', required=True, max_length=10)
    country = forms.CharField(label='País', required=False, max_length=150)
    uf = forms.CharField(label='UF', required=True, max_length=150)
    city = forms.CharField(label='Cidade', required=True, max_length=150)
    neighborhood = forms.CharField(label='Bairro', required=False, max_length=100)
    address = forms.CharField(label='Endereço', required=False, max_length=300)
    phone = forms.CharField(label='Telefone', required=True, max_length=30)
    allergy = forms.CharField(label='Alergia', required=False, max_length=500)
    federation = forms.ModelChoiceField(label='Federação afiliado', required=False, queryset=Federation.objects.all())
    name_emergency_contact = forms.CharField(label='Nome de contato emergencial', required=True, max_length=150)
    emergency_phone = forms.CharField(label='Telefone contato emergencial', required=True, max_length=30)
    blood_type = forms.ChoiceField(label='Tipo sanguineo', required=False, choices=CHOICE_BLOOD_TYPE)
    national_license = forms.CharField(label='Licença nacional', required=False, max_length=150)
    health_insurance_plan = forms.CharField(label='Plano de saúde', required=False, max_length=150)
    cnh = forms.CharField(label='CNH', required=False, max_length=150)
    lgpd_acceptance = forms.BooleanField(label='Aceite LGPD', required=False)
    email = forms.EmailField(label='E-mail', required=False, max_length=150)
    type = forms.ModelChoiceField(label='Tipo', required=True, queryset=TypeCompetitor.objects.none())
    thermo = forms.BooleanField(label='Termo de Responsabilidade', required=True)

    class Meta:
        model = CompetitorsRegistration
        fields = '__all__'

    def __init__(self, missing_types, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = TypeCompetitor.objects.filter(id__in=missing_types)
        self.fields['full_name'] = forms.CharField(label='Full Name', max_length=100)

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not CPF().validate(cpf):
            raise forms.ValidationError("CPF inválido")
        return cpf

    def clean_cnh(self):
        if self.cleaned_data['cnh'] is not None and self.cleaned_data['cnh'] != '':
            cnh = self.cleaned_data['cnh']
            if not CNH().validate(cnh):
                raise forms.ValidationError("CNH inválida")
            return cnh


# Cadastro para o zequinha ou apoio, estendendo o form de competidor e sobrescrevendo alguns campos
class ZequinhaApoioForm(CompetitorRegistrationForm):
    type = forms.ModelChoiceField(label='Tipo', required=False, queryset=TypeCompetitor.objects.none())

    class Meta:
        model = CompetitorsRegistration
        fields = '__all__'
        exclude = ('type', )
    # def __init__(self, missing_types, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['type'].queryset = TypeCompetitor.objects.none()


class RegistrationDocumentsForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    # user = forms.CharField(required=False, max_length=500)
    competitor_registration = forms.ModelChoiceField(queryset=None, required=False)
    document_type = forms.ModelChoiceField(queryset=None, required=False)

    class Meta:
        model = RegistrationDocuments
        fields = ['user', 'competitor_registration', 'document_type', 'document_file']


class UserProfileForm(forms.ModelForm):
    nickname = forms.CharField(label='Apelido', required=True, max_length=150)
    clothing = forms.ChoiceField(label='Vestuário', required=True, choices=CHOICE_CLOTHING)
    cep = forms.CharField(label='CEP', required=True, max_length=10)
    country = forms.CharField(label='País', required=True, max_length=150)
    uf = forms.CharField(label='UF', required=True, max_length=150)
    city = forms.CharField(label='Cidade', required=True, max_length=150)
    neighborhood = forms.CharField(label='Bairro', required=True, max_length=100)
    address = forms.CharField(label='Endereço', required=True, max_length=300)
    phone = forms.CharField(label='Telefone', required=True, max_length=30)
    allergy = forms.CharField(label='Alergia', required=False, max_length=500)
    federation = forms.ModelChoiceField(label='Federação afiliado', required=False, queryset=Federation.objects.all())
    name_emergency_contact = forms.CharField(label='Nome de contato emergencial', required=True, max_length=150)
    blood_type = forms.ChoiceField(label='Tipo sanguineo', required=True, choices=CHOICE_BLOOD_TYPE)
    # national_license = forms.CharField(label='Licença nacional', required=True, max_length=150)
    # health_insurance_plan = forms.CharField(label='Plano de saúde', required=True, max_length=150)

    class Meta:
        model = User
        exclude = (
            'username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions', 'last_login', 'date_joined', 'rg', 'cpf', 'organ_expedidor', 'birthdate',
            'national_license', 'cnh', 'lgpd_acceptance', 'customer'
        )
