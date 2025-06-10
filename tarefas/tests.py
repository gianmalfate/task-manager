
from django.test import TestCase
from datetime import date, timedelta
from django.urls import reverse
from .models import Tarefa, Categoria



class ListasBuscaTests(TestCase):
    def setUp(self):
        hoje     = date.today()
        amanha   = hoje + timedelta(days=1)
        trabalho = Categoria.objects.create(nome="Trabalho")
        lazer    = Categoria.objects.create(nome="Lazer")

        Tarefa.objects.create(  # pendente-alta
            titulo="Enviar email urgente",
            descricao="Responder cliente",
            data=amanha, prioridade="alta",
            status="pendente", categoria=trabalho,
        )
        Tarefa.objects.create(  # pendente-baixa
            titulo="Planejar férias",
            descricao="Ver passagens",
            data=amanha, prioridade="baixa",
            status="pendente", categoria=lazer,
        )
        Tarefa.objects.create(  # concluída
            titulo="Relatório final",
            descricao="PDF enviado",
            data=hoje, prioridade="média",
            status="concluído", categoria=trabalho,
        )
        Tarefa.objects.create(  # adiada
            titulo="Comprar presentes",
            descricao="Lembrar de promoções",
            data=hoje, prioridade="média",
            status="adiado", categoria=lazer,
        )

    # 1 ─ Busca por termo em pendentes
    def test_busca_pendentes(self):
        url = reverse("tarefas_pendentes_list") + "?q=email"
        resp = self.client.get(url)
        self.assertContains(resp, "Enviar email urgente")
        self.assertNotContains(resp, "Planejar férias")  # termo não aparece
        self.assertEqual(resp.context["tarefas_pendentes"].count(), 1)

    # 2 ─ Busca por termo em concluídas
    def test_busca_concluidas(self):
        url = reverse("tarefas_concluidas_list") + "?q=relatório"
        resp = self.client.get(url)
        self.assertContains(resp, "Relatório final")
        self.assertEqual(resp.context["tarefas_concluidas"].count(), 1)

    # 3 ─ Filtro por categoria em pendentes
    def test_filtro_categoria(self):
        lazer = Categoria.objects.get(nome="Lazer").id
        url = reverse("tarefas_pendentes_list") + f"?categoria={lazer}"
        resp = self.client.get(url)
        self.assertContains(resp, "Planejar férias")
        self.assertNotContains(resp, "Enviar email urgente")

    # 4 ─ Ordenação por prioridade (alta deve vir antes de baixa)
    def test_ordenar_por_prioridade(self):
        url = reverse("tarefas_pendentes_list") + "?ordenar_por=prioridade"
        resp = self.client.get(url)
        tarefas = list(resp.context["tarefas_pendentes"])
        self.assertEqual(tarefas[0].prioridade, "alta")
        self.assertEqual(tarefas[1].prioridade, "baixa")

    # 5 ─ Busca vazia devolve todas as pendentes
    def test_busca_vazia(self):
        url = reverse("tarefas_pendentes_list")  # sem q=
        resp = self.client.get(url)
        self.assertEqual(resp.context["tarefas_pendentes"].count(), 2)