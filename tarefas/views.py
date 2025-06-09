from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa, Categoria
from .forms import TarefaForm, CategoriaForm
from datetime import date, datetime, timedelta
from django.db.models import Case, When, Value, IntegerField
import calendar


def tarefas_pendentes_list(request):
    categoria_id = request.GET.get('categoria')
    ordenar_por = request.GET.get('ordenar_por', 'data')
    tarefas_pendentes = Tarefa.objects.filter(status="pendente")
    if categoria_id:
        tarefas_pendentes = tarefas_pendentes.filter(categoria_id=categoria_id)
    if ordenar_por == 'prioridade':
        tarefas_pendentes = tarefas_pendentes.annotate(
            prioridade_order=Case(
                When(prioridade='alta', then=Value(1)),
                When(prioridade='média', then=Value(2)),
                When(prioridade='baixa', then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by('prioridade_order', 'data')
    else:
        tarefas_pendentes = tarefas_pendentes.order_by('data', 'prioridade')

    categorias = Categoria.objects.all()
    context = {
        'tarefas_pendentes': tarefas_pendentes,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'ordenar_por': ordenar_por,
        'today': date.today(),
    }
    return render(request, "tarefas/tarefas_pendentes.html", context)

def adicionar_tarefa(request):
    data_inicial = request.GET.get('data')
    if request.method == "POST":
        form = TarefaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("tarefas_pendentes_list")
    else:
        form = TarefaForm()
        form.fields["titulo"].initial = ""
        if data_inicial:
            form.fields["data"].initial = data_inicial
            form.fields["data"].widget = form.fields["data"].hidden_widget()

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
    ordenar_por = request.GET.get('ordenar_por', 'data')
    tarefas_concluidas = Tarefa.objects.filter(status="concluído")
    if categoria_id:
        tarefas_concluidas = tarefas_concluidas.filter(categoria_id=categoria_id)
    if ordenar_por == 'prioridade':
        tarefas_concluidas = tarefas_concluidas.annotate(
            prioridade_order=Case(
                When(prioridade='alta', then=Value(1)),
                When(prioridade='média', then=Value(2)),
                When(prioridade='baixa', then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by('prioridade_order', 'data')
    else:
        tarefas_concluidas = tarefas_concluidas.order_by('data', 'prioridade')

    categorias = Categoria.objects.all()
    context = {
        'tarefas_concluidas': tarefas_concluidas,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'ordenar_por': ordenar_por,
        'today': date.today(),
    }
    return render(request, "tarefas/tarefas_concluidas.html", context)


def tarefas_adiadas_list(request):
    categoria_id = request.GET.get('categoria')
    ordenar_por = request.GET.get('ordenar_por', 'data')
    tarefas_adiadas = Tarefa.objects.filter(status="adiado")
    if categoria_id:
        tarefas_adiadas = tarefas_adiadas.filter(categoria_id=categoria_id)
    if ordenar_por == 'prioridade':
        tarefas_adiadas = tarefas_adiadas.annotate(
            prioridade_order=Case(
                When(prioridade='alta', then=Value(1)),
                When(prioridade='média', then=Value(2)),
                When(prioridade='baixa', then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by('prioridade_order', 'data')
    else:
        tarefas_adiadas = tarefas_adiadas.order_by('data', 'prioridade')

    categorias = Categoria.objects.all()
    context = {
        'tarefas_adiadas': tarefas_adiadas,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'ordenar_por': ordenar_por,
        'today': date.today(),
    }
    return render(request, "tarefas/tarefas_adiadas.html", context)


def mover_para_tarefas(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.status = "pendente"
    tarefa.save()

    return redirect("tarefas_pendentes_list")

#view de calendário que exiba as tarefas pendentes em um calendário mensal

def calendario_mensal(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Generate calendar grid for the month
    month_days = calendar.Calendar(firstweekday=6).monthdatescalendar(year, month)

    # Fetch all pending tasks
    tarefas = Tarefa.objects.filter(status='pendente')

    # Organize pending tasks per day 
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            tarefas_do_dia = tarefas.filter(data=day)
            week_data.append({
                'day': day,
                'is_current_month': day.month == month,
                'pendentes': tarefas_do_dia,
            })
        calendar_data.append(week_data)
    
    #set indicator for the current day
    for week in calendar_data:
        for day_data in week:
            day_data['is_today'] = (day_data['day'] == today)
    

    # Calculate previous and next month for navigation
    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, calendar.monthrange(year, month)[1])

    prev_month = (first_day_of_month - timedelta(days=1)).replace(day=1)
    next_month = (last_day_of_month + timedelta(days=1)).replace(day=1)

    context = {
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'prev_year': prev_month.year,
        'prev_month': prev_month.month,
        'next_year': next_month.year,
        'next_month': next_month.month,
    }

    return render(request, 'tarefas/calendario_mensal.html', context)
