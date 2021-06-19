from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.choices import LOGRADOURO_CHOICES, UF_CHOICES
from datetime import datetime


class EmailUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        email = kwargs["email"]
        email = self.normalize_email(email)
        password = kwargs["password"]
        kwargs.pop("password")

        if not email:
            raise ValueError(_('Necessário um email válido'))

        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class ParametrosOS(models.Model):
    descricao = models.CharField(max_length=30, blank=True, null=True)
    data_inicial = models.CharField(max_length=10, blank=False)
    data_final = models.CharField(max_length=10, blank=False)
    nivel_func = models.CharField(verbose_name=_('Nível Funcionario'), max_length=10, blank=False, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Parametros'

    def __str__(self):
        return "{} | {} | {} | {}".format(self.id, self.descricao, self.data_inicial , self.data_final)

    def __repr__(self):
        return "{} | {} | {} | {}".format(self.id, self.descricao, self.data_inicial , self.data_final)


class Equipes(models.Model):
    nome_equipe = models.CharField(max_length=200, blank=True, null=True)
    coordenador = models.CharField(max_length=255, blank=True, null=True)
    qtdIntegrante = models.IntegerField(default=0, blank=True, null=True)
    integrantes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Equipe'

    def __str__(self):
        return "{} | {}".format(self.id, self.nome_equipe)

    def __repr__(self):
        return "{} | {}".format(self.id, self.nome_equipe)


class Feriado(models.Model):
    feriado = models.CharField(max_length=200, blank=True, null=True)
    dia_mes_ano = models.DateTimeField(default=datetime.now, blank=False)
    cidade = models.CharField(verbose_name= 'cidade', max_length=50, blank=True, null=True)
    local = models.CharField(verbose_name= 'local', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Feriado'

    def __str__(self):
        return "{} | {}".format(self.id, self.feriado)

    def __repr__(self):
        return "{} | {}".format(self.id, self.feriado)


# OS - FUNCIONARIOS
class MyUser(PermissionsMixin, AbstractBaseUser):
    nome = models.CharField(verbose_name=_('Nome Funcionario'), max_length=20, blank=False)
    sobrenome = models.CharField(verbose_name=_('Sobrenome'), max_length=100, blank=False)
    email = models.EmailField(verbose_name=_('Email'), unique=True, max_length=100)
    cpf = models.CharField(verbose_name=_('CPF'), max_length=14, blank=True, null=True)
    celular = models.CharField(verbose_name=_('Numero de Telefone'), max_length=11, blank=False, null=True)
    nivel_funcionario = models.CharField(verbose_name=_('Nível Funcionario'), max_length=10, blank=True)
    coordenador = models.CharField(max_length=20, blank=True)
    selfie_usuario = CloudinaryField('self_usuario', blank=False, null=True)
    data_nasc = models.CharField(max_length=12, blank=False, null=False)
    cep = models.CharField(max_length=9, blank=True, null=True)
    logradouro = models.CharField(max_length=75, blank=True, null=True)
    numero = models.CharField(max_length=6, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=UF_CHOICES, default='0')

    reset_pass = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    objects = EmailUserManager()

    class Meta:
        db_table = 'MyUser'

    def __str__(self):
        return "{} | {}".format(self.id, self.nome)

    def __repr__(self):
        return "{} | {}".format(self.id, self.nome)

    @property
    def ativo_human(self):
        return 'Sim' if self.is_active else 'Não'


# for user in MyUser.objects.all():
#     Token.objects.get_or_create(user=user)


# OS - CLIENTE
class Clientes(models.Model):
    nome_empresa = models.CharField(verbose_name=_("Nome da Empresa"), max_length=20, unique=True, blank=False, null=True)
    telefone_empresa = models.CharField(verbose_name=_("Contato da Empresa"), max_length=15, blank=False, null=True)
    email = models.EmailField(verbose_name=_("Email"), max_length=255, blank=False, null=True)
    logomarca = CloudinaryField('logomarca', blank=True, null=True)
    razao_social = models.CharField(max_length=100,blank=False, null=True)
    nome_fantasia = models.CharField(max_length=50, blank=False, null=True)
    cnpj = models.CharField(verbose_name=_('CNPJ'), max_length=20, blank=False, null=True)
    insc_estad = models.CharField(verbose_name=_('IE'), max_length=20, blank=True,null=True)
    cep = models.CharField(max_length=9, blank=False, null=True),
    tipo_logradouro = models.CharField(max_length=3, choices=LOGRADOURO_CHOICES, default='0')
    logradouro = models.CharField(max_length=75, blank=False, null=True)
    numero = models.CharField(max_length=6, blank=False, null=True)
    bairro = models.CharField(max_length=100, blank=False, null=True)
    complemento = models.CharField(max_length=100, blank=False, null=True)
    municipio = models.CharField(max_length=50, blank=False, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True, choices=UF_CHOICES, default='0')

    data_registro = models.DateField(auto_now_add=True)

    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return "{} | {}".format(self.id, self.nome_empresa)

    def __repr__(self):
        return "{} | {}".format(self.id, self.nome_empresa)


class Projetos(models.Model):
    nome_projeto = models.CharField(verbose_name='nome projeto', max_length=20, blank=False, null=True)

    # Amarrado com a tabela de usuarios (MyUser)
    # Filtrar os dados dos usuarios
    myuser = models.ForeignKey(MyUser, blank=False, null=True, on_delete=models.CASCADE)

    # Amarrado com a tabela de cliente (Cliente)
    # Filtrar os dados dos cliente
    clientes = models.ForeignKey(Clientes, blank=False, null=True, on_delete=models.CASCADE)

    solicitante = models.CharField(verbose_name=_('Solicitante'), max_length=20, blank=False, null=True)

    # Amarrado com a tabela de equipes (Equipe)
    # Filtrar os dados da equipe
    equipes = models.ForeignKey(Equipes, blank=True, null=False, on_delete=models.CASCADE)

    anexo_projeto = CloudinaryField('anexo_projeto', blank=True, null=True)

    data_horario_inicio = models.CharField(max_length=12, blank=False, null=False)
    data_horario_conclusao = models.CharField(max_length=12, blank=False, null=False)

    observacao = models.CharField(verbose_name='observação', max_length=20, blank=False, null=True)
    ativo = models.BooleanField(default=True, blank=False)

    class Meta:
        db_table = 'Projetos'

    def __str__(self):
        return "{} | {}".format(self.id, self.nome_projeto)

    def __repr__(self):
        return "{} | {}".format(self.id, self.nome_projeto)


#OS - SERVIÇOS
class CadastroOS(models.Model):
    # Amarrado com a tabela de usuarios (MyUser)
    # Filtrar os dados dos usuarios
    myuser = models.ForeignKey(MyUser, blank=False, null=True, on_delete=models.CASCADE)

    # Amarrado com a tabela de projetos (Projetos)
    # Filtrar os dados dos projetos
    projetos = models.ForeignKey(Projetos, blank=False, null=True, on_delete=models.CASCADE)

    # Amarrado com a tabela de cliente (Cliente)
    # Filtrar os dados dos clientes
    clientes = models.ForeignKey(Clientes, blank=False, null=True, on_delete=models.CASCADE)

    # Amarrado com a tabela de equipes (Equipe)
    # Filtrar os dados das equipes
    equipes = models.ForeignKey(Equipes, blank=False, null=True, on_delete=models.CASCADE)

    anexo_cliente = CloudinaryField('anexo_cliente', blank=True, null=True)

    solicitante = models.CharField(verbose_name='Solicitante', max_length=20, blank=True, null=True)
    traslado = models.TimeField(_(u"Conversation Time"), auto_now_add=True, blank=True)
    desconto = models.FloatField(default=0, blank=False, null=True)
    h50 = models.TimeField(_(u"Conversation Time"), auto_now_add=False, blank=True)
    h100 = models.TimeField(_(u"Conversation Time"), auto_now_add=False, blank=True)
    total = models.TimeField(_(u"Conversation Time"), auto_now_add=False, blank=True)
    valor = models.FloatField(default=0, blank=True, null=True)

    horas_hoje = models.TimeField(_(u"Conversation Time"), auto_now_add=False, blank=True)
    data_horario_inicio = models.CharField(max_length=12, blank=False, null=False)
    data_horario_conclusao = models.CharField(max_length=12, blank=False, null=False)

    observacao = models.CharField(verbose_name='observação', max_length=20, blank=True, null=True)
    anexo = CloudinaryField('anexo', blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'CadastroOS'

    def __str__(self):
        return "{} | {}".format(self.id, self.projetos.pk if self.projetos else '')

    def __repr__(self):
        return "{} | {}".format(self.id, self.projetos.pk if self.projetos else '')


# Automatizando a criação do token para cada usuario
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)





