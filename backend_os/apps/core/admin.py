from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CadastroOS)
admin.site.register(models.MyUser)
admin.site.register(models.ParametrosOS)
admin.site.register(models.Clientes)
admin.site.register(models.Projetos)
admin.site.register(models.Feriado)
admin.site.register(models.Equipes)