from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50, default="Geral")

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    OPCOES_PRIORIDADE = (
        ("alta", "Alta"),
        ("média", "Média"),
        ("baixa", "Baixa"),
    )
    OPCOES_STATUS = (
        ("concluído", "Concluído"),
        ("pendente", "Pendente"),
        ("adiado", "Adiado"),
    )

    titulo = models.CharField(max_length=50, default="Sem título")
    descricao = models.CharField(max_length=400)
    data = models.DateField()
    prioridade = models.CharField(max_length=25, choices=OPCOES_PRIORIDADE, default="média")
    status = models.CharField(max_length=25, choices=OPCOES_STATUS, default="pendente")
    categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.CASCADE,
        related_name="tarefas",
    )

    def __str__(self):
        return self.titulo
