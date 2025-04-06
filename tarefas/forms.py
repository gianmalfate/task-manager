from django import forms
from datetime import date
from .models import Tarefa, Categoria


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ("titulo", "descricao", "data", "prioridade", "categoria")
        widgets = {
            'data': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': date.today().strftime('%Y-%m-%d')  # Define o mínimo para hoje
                }
            ),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ("nome",)
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Digite o nome da categoria"})
        }