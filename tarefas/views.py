from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa, Categoria
from .forms import TarefaForm, CategoriaForm
from datetime import date
from django.db.models import Case, When, Value, IntegerField, Q


def tarefas_pendentes_list(request):
    busca = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria")
    ordenar_por = request.GET.get("ordenar_por", "data")
    tarefas_pendentes = Tarefa.objects.filter(status="pendente")
    if busca:
        tarefas_pendentes = tarefas_pendentes.filter(
            Q(titulo__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(categoria__nome__icontains=busca)
        )
    if categoria_id:
        tarefas_pendentes = tarefas_pendentes.filter(categoria_id=categoria_id)
    if ordenar_por == "prioridade":
        tarefas_pendentes = tarefas_pendentes.annotate(
            prioridade_order=Case(
                When(prioridade="alta", then=Value(1)),
                When(prioridade="média", then=Value(2)),
                When(prioridade="baixa", then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by("prioridade_order", "data")
    else:
        tarefas_pendentes = tarefas_pendentes.order_by("data", "prioridade")

    categorias = Categoria.objects.all()
    context = {
        "tarefas_pendentes": tarefas_pendentes,
        "categorias": categorias,
        "categoria_selecionada": categoria_id,
        "ordenar_por": ordenar_por,
        "today": date.today(),
        "q": busca,
    }
    return render(request, "tarefas/tarefas_pendentes.html", context)


def adicionar_tarefa(request):
    if request.method == "POST":
        form = TarefaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("tarefas_pendentes_list")
    else:
        form = TarefaForm()
        form.fields["titulo"].initial = ""  # Define o campo vazio diretamente no view

    return render(request, "tarefas/adicionar_tarefa.html", {"form": form})


def criar_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("tarefas_pendentes_list")
    else:
        form = CategoriaForm()
        form.fields["nome"].initial = ""  # Define o campo vazio diretamente no view

    return render(request, "categorias/criar_categoria.html", {"form": form})


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
        form = TarefaForm(
            request.POST, instance=tarefa
        )  # Use o instance para vincular ao objeto
        if form.is_valid():
            form.save()  # Salva diretamente todos os campos do formulário no objeto
            return redirect("tarefas_pendentes_list")
    else:
        form = TarefaForm(
            instance=tarefa
        )  # Preenche o formulário com os valores atuais

    return render(
        request, "tarefas/editar_tarefa.html", {"tarefa": tarefa, "form": form}
    )


def tarefas_concluidas_list(request):
    busca = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria")
    ordenar_por = request.GET.get("ordenar_por", "data")
    tarefas_concluidas = Tarefa.objects.filter(status="concluído")
    if busca:
        tarefas_concluidas = tarefas_concluidas.filter(
            Q(titulo__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(categoria__nome__icontains=busca)
        )

    if categoria_id:
        tarefas_concluidas = tarefas_concluidas.filter(categoria_id=categoria_id)
    if ordenar_por == "prioridade":
        tarefas_concluidas = tarefas_concluidas.annotate(
            prioridade_order=Case(
                When(prioridade="alta", then=Value(1)),
                When(prioridade="média", then=Value(2)),
                When(prioridade="baixa", then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by("prioridade_order", "data")
    else:
        tarefas_concluidas = tarefas_concluidas.order_by("data", "prioridade")

    categorias = Categoria.objects.all()
    context = {
        "tarefas_concluidas": tarefas_concluidas,
        "categorias": categorias,
        "categoria_selecionada": categoria_id,
        "ordenar_por": ordenar_por,
        "today": date.today(),
        "q": busca,
    }
    return render(request, "tarefas/tarefas_concluidas.html", context)


def tarefas_adiadas_list(request):
    busca = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria")
    ordenar_por = request.GET.get("ordenar_por", "data")
    tarefas_adiadas = Tarefa.objects.filter(status="adiado")
    if busca:
        tarefas_adiadas = tarefas_adiadas.filter(
            Q(titulo__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(categoria__nome__icontains=busca)
        )
    if categoria_id:
        tarefas_adiadas = tarefas_adiadas.filter(categoria_id=categoria_id)
    if ordenar_por == "prioridade":
        tarefas_adiadas = tarefas_adiadas.annotate(
            prioridade_order=Case(
                When(prioridade="alta", then=Value(1)),
                When(prioridade="média", then=Value(2)),
                When(prioridade="baixa", then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by("prioridade_order", "data")
    else:
        tarefas_adiadas = tarefas_adiadas.order_by("data", "prioridade")

    categorias = Categoria.objects.all()
    context = {
        "tarefas_adiadas": tarefas_adiadas,
        "categorias": categorias,
        "categoria_selecionada": categoria_id,
        "ordenar_por": ordenar_por,
        "today": date.today(),
        "q": busca,
    }
    return render(request, "tarefas/tarefas_adiadas.html", context)


def mover_para_tarefas(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = "pendente"
    tarefa.save()

    return redirect("tarefas_pendentes_list")
