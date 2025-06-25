from django.contrib import admin

from .models import Categoria, Tarefa

admin.site.register(Tarefa)
admin.site.register(Categoria)
