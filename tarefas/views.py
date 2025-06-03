from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa, Categoria
from .forms import TarefaForm, CategoriaForm
from datetime import date


def tarefas_pendentes_list(request):
    categoria_id = request.GET.get('categoria')
    tarefas_pendentes = Tarefa.objects.filter(status="pendente")
    if categoria_id:
        tarefas_pendentes = tarefas_pendentes.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()
    context = {
        'tarefas_pendentes': tarefas_pendentes,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'today': date.today(),  # Adiciona a data atual ao contexto
    }

    return render(request, "tarefas/tarefas_pendentes.html",
                  context)

def adicionar_tarefa(request):
    if request.method == "POST":
        form = TarefaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("tarefas_pendentes_list")
    else:
        form = TarefaForm()
        form.fields["titulo"].initial = ""  # Define o campo vazio diretamente no view

    return render(request, "tarefas/adicionar_tarefa.html",
                  {"form": form})

def criar_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("tarefas_pendentes_list")
    else:
        form = CategoriaForm()
        form.fields["nome"].initial = ""  # Define o campo vazio diretamente no view

    return render(request, "categorias/criar_categoria.html",
                  {"form": form})

def concluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = "concluído"
    tarefa.save()

    return redirect("tarefas_pendentes_list")


def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.delete()

    return redirect("tarefas_pendentes_list")


def adiar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = "adiado"
    tarefa.save()

    return redirect("tarefas_pendentes_list")


def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)

    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)  # Use o instance para vincular ao objeto
        if form.is_valid():
            form.save()  # Salva diretamente todos os campos do formulário no objeto
            return redirect("tarefas_pendentes_list")
    else:
        form = TarefaForm(instance=tarefa)  # Preenche o formulário com os valores atuais

    return render(request, "tarefas/editar_tarefa.html", {"tarefa": tarefa, "form": form})


def tarefas_concluidas_list(request):
    categoria_id = request.GET.get('categoria')
    tarefas_concluidas = Tarefa.objects.filter(status="concluído")
    if categoria_id:
        tarefas_concluidas = tarefas_concluidas.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()

    context = {
        'tarefas_concluidas': tarefas_concluidas,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'today': date.today(),  # Adiciona a data atual ao contexto
    }

    return render(request, "tarefas/tarefas_concluidas.html", context)


def tarefas_adiadas_list(request):
    categoria_id = request.GET.get('categoria')
    tarefas_adiadas = Tarefa.objects.filter(status="adiado")
    if categoria_id:
        tarefas_adiadas = tarefas_adiadas.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()

    context = {
        'tarefas_adiadas': tarefas_adiadas,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'today': date.today(),  # Adiciona a data atual ao contexto
    }

    return render(request, "tarefas/tarefas_adiadas.html", context)


def mover_para_tarefas(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = "pendente"
    tarefa.save()

    return redirect("tarefas_pendentes_list")