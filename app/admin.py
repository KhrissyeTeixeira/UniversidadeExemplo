from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Aluno, Professor, Turma, Aula, Presenca, Matricula, Usuario

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(Aula)
admin.site.register(Presenca)
admin.site.register(Matricula)
admin.site.register(Usuario, UserAdmin)