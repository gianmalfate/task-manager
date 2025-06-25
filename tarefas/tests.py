from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from .forms import CategoriaForm, TarefaForm
from .models import Categoria, Tarefa

# =============================================
# TESTES DOS MODELOS
# =============================================


class TarefaModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Trabalho")

    def test_criar_tarefa_com_todos_campos(self):
        """Testa criação de tarefa com todos os campos preenchidos"""
        tarefa = Tarefa.objects.create(
            titulo="Reunião importante",
            descricao="Discussão sobre o projeto X",
            data=date.today() + timedelta(days=1),
            prioridade="alta",
            status="pendente",
            categoria=self.categoria,
        )

        self.assertEqual(tarefa.titulo, "Reunião importante")
        self.assertEqual(tarefa.descricao, "Discussão sobre o projeto X")
        self.assertEqual(tarefa.prioridade, "alta")
        self.assertEqual(tarefa.status, "pendente")
        self.assertEqual(tarefa.categoria, self.categoria)
        self.assertTrue(isinstance(tarefa.data, date))

    def test_criar_tarefa_com_campos_padrao(self):
        """Testa criação de tarefa com valores padrão"""
        tarefa = Tarefa.objects.create(
            descricao="Tarefa simples", data=date.today(), categoria=self.categoria
        )

        self.assertEqual(tarefa.titulo, "Sem título")  # valor padrão
        self.assertEqual(tarefa.prioridade, "média")  # valor padrão
        self.assertEqual(tarefa.status, "pendente")  # valor padrão

    def test_opcoes_prioridade_validas(self):
        """Testa se as opções de prioridade estão funcionando"""
        prioridades = ["alta", "média", "baixa"]

        for prioridade in prioridades:
            tarefa = Tarefa.objects.create(
                descricao=f"Tarefa {prioridade}",
                data=date.today(),
                prioridade=prioridade,
                categoria=self.categoria,
            )
            self.assertEqual(tarefa.prioridade, prioridade)

    def test_opcoes_status_validas(self):
        """Testa se as opções de status estão funcionando"""
        status_opcoes = ["concluído", "pendente", "adiado"]

        for status in status_opcoes:
            tarefa = Tarefa.objects.create(
                descricao=f"Tarefa {status}",
                data=date.today(),
                status=status,
                categoria=self.categoria,
            )
            self.assertEqual(tarefa.status, status)

    def test_str_method_tarefa(self):
        """Testa o método __str__ da Tarefa"""
        tarefa = Tarefa.objects.create(
            titulo="Tarefa Teste",
            descricao="Descrição teste",
            data=date.today(),
            categoria=self.categoria,
        )
        self.assertEqual(str(tarefa), "Tarefa Teste")

    def test_relacionamento_categoria_tarefa(self):
        """Testa o relacionamento entre Categoria e Tarefa"""
        tarefa1 = Tarefa.objects.create(
            titulo="Tarefa 1",
            descricao="Primeira tarefa",
            data=date.today(),
            categoria=self.categoria,
        )
        tarefa2 = Tarefa.objects.create(
            titulo="Tarefa 2",
            descricao="Segunda tarefa",
            data=date.today(),
            categoria=self.categoria,
        )

        # Testa se a categoria tem as tarefas relacionadas
        self.assertEqual(self.categoria.tarefas.count(), 2)
        self.assertIn(tarefa1, self.categoria.tarefas.all())
        self.assertIn(tarefa2, self.categoria.tarefas.all())


class CategoriaModelTests(TestCase):
    def test_criar_categoria(self):
        """Testa criação de categoria"""
        categoria = Categoria.objects.create(nome="Estudos")
        self.assertEqual(categoria.nome, "Estudos")

    def test_categoria_com_valor_padrao(self):
        """Testa criação de categoria com valor padrão"""
        categoria = Categoria.objects.create()
        self.assertEqual(categoria.nome, "Geral")

    def test_str_method_categoria(self):
        """Testa o método __str__ da Categoria"""
        categoria = Categoria.objects.create(nome="Pessoal")
        self.assertEqual(str(categoria), "Pessoal")


# =============================================
# TESTES DAS VIEWS
# =============================================


class TarefaViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nome="Trabalho")
        self.tarefa_pendente = Tarefa.objects.create(
            titulo="Tarefa Pendente",
            descricao="Descrição da tarefa pendente",
            data=date.today() + timedelta(days=1),
            prioridade="alta",
            status="pendente",
            categoria=self.categoria,
        )
        self.tarefa_concluida = Tarefa.objects.create(
            titulo="Tarefa Concluída",
            descricao="Descrição da tarefa concluída",
            data=date.today(),
            prioridade="média",
            status="concluído",
            categoria=self.categoria,
        )

    def test_lista_tarefas_pendentes_get(self):
        """Testa se a view de tarefas pendentes carrega corretamente"""
        url = reverse("tarefas_pendentes_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarefa Pendente")
        self.assertNotContains(response, "Tarefa Concluída")
        self.assertEqual(len(response.context["tarefas_pendentes"]), 1)

    def test_adicionar_tarefa_get(self):
        """Testa se a página de adicionar tarefa carrega corretamente"""
        url = reverse("adicionar_tarefa")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], TarefaForm)

    def test_adicionar_tarefa_post_valido(self):
        """Testa criação de tarefa via POST com dados válidos"""
        url = reverse("adicionar_tarefa")
        data = {
            "titulo": "Nova Tarefa",
            "descricao": "Descrição da nova tarefa",
            "data": date.today() + timedelta(days=1),
            "prioridade": "média",
            "categoria": self.categoria.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(Tarefa.objects.filter(titulo="Nova Tarefa").exists())

    def test_concluir_tarefa(self):
        """Testa a funcionalidade de concluir tarefa"""
        url = reverse("concluir_tarefa", args=[self.tarefa_pendente.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # redirect
        self.tarefa_pendente.refresh_from_db()
        self.assertEqual(self.tarefa_pendente.status, "concluído")

    def test_excluir_tarefa(self):
        """Testa a funcionalidade de excluir tarefa"""
        tarefa_id = self.tarefa_pendente.id
        url = reverse("excluir_tarefa", args=[tarefa_id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # redirect
        self.assertFalse(Tarefa.objects.filter(id=tarefa_id).exists())

    def test_adiar_tarefa(self):
        """Testa a funcionalidade de adiar tarefa"""
        url = reverse("adiar_tarefa", args=[self.tarefa_pendente.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # redirect
        self.tarefa_pendente.refresh_from_db()
        self.assertEqual(self.tarefa_pendente.status, "adiado")

    def test_editar_tarefa_get(self):
        """Testa se a página de editar tarefa carrega com dados da tarefa"""
        url = reverse("editar_tarefa", args=[self.tarefa_pendente.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertEqual(form.instance.titulo, self.tarefa_pendente.titulo)

    def test_editar_tarefa_post(self):
        """Testa edição de tarefa via POST"""
        url = reverse("editar_tarefa", args=[self.tarefa_pendente.id])
        data = {
            "titulo": "Título Editado",
            "descricao": "Descrição editada",
            "data": self.tarefa_pendente.data,
            "prioridade": "baixa",
            "categoria": self.categoria.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # redirect
        self.tarefa_pendente.refresh_from_db()
        self.assertEqual(self.tarefa_pendente.titulo, "Título Editado")
        self.assertEqual(self.tarefa_pendente.prioridade, "baixa")

    def test_criar_categoria_get(self):
        """Testa se a página de criar categoria carrega corretamente"""
        url = reverse("criar_categoria")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CategoriaForm)

    def test_criar_categoria_post(self):
        """Testa criação de categoria via POST"""
        url = reverse("criar_categoria")
        data = {"nome": "Nova Categoria"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(Categoria.objects.filter(nome="Nova Categoria").exists())


# =============================================
# TESTES DOS FORMULÁRIOS
# =============================================


class TarefaFormTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Teste")

    def test_formulario_tarefa_valido(self):
        """Testa formulário de tarefa com dados válidos"""
        form_data = {
            "titulo": "Tarefa Teste",
            "descricao": "Descrição de teste",
            "data": date.today() + timedelta(days=1),
            "prioridade": "alta",
            "categoria": self.categoria.id,
        }
        form = TarefaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_tarefa_titulo_obrigatorio(self):
        """Testa se o campo título é obrigatório no formulário"""
        form_data = {
            "titulo": "",  # título vazio
            "descricao": "Descrição de teste",
            "data": date.today() + timedelta(days=1),
            "prioridade": "média",
            "categoria": self.categoria.id,
        }
        form = TarefaForm(data=form_data)
        # O formulário deve ser inválido se o título estiver vazio
        self.assertFalse(form.is_valid())
        self.assertIn("titulo", form.errors)

    def test_formulario_tarefa_sem_descricao(self):
        """Testa formulário sem descrição (campo obrigatório)"""
        form_data = {
            "titulo": "Tarefa Teste",
            "data": date.today() + timedelta(days=1),
            "prioridade": "média",
            "categoria": self.categoria.id,
        }
        form = TarefaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)

    def test_formulario_tarefa_sem_data(self):
        """Testa formulário sem data (campo obrigatório)"""
        form_data = {
            "titulo": "Tarefa Teste",
            "descricao": "Descrição de teste",
            "prioridade": "média",
            "categoria": self.categoria.id,
        }
        form = TarefaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("data", form.errors)

    def test_formulario_tarefa_sem_categoria(self):
        """Testa formulário sem categoria (campo obrigatório)"""
        form_data = {
            "titulo": "Tarefa Teste",
            "descricao": "Descrição de teste",
            "data": date.today() + timedelta(days=1),
            "prioridade": "média",
        }
        form = TarefaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("categoria", form.errors)

    def test_formulario_tarefa_data_passada(self):
        """Testa se o widget de data tem restrição para datas passadas"""
        form = TarefaForm()
        data_widget = form.fields["data"].widget
        min_date = data_widget.attrs.get("min")
        self.assertEqual(min_date, date.today().strftime("%Y-%m-%d"))

    def test_formulario_tarefa_prioridade_invalida(self):
        """Testa formulário com prioridade inválida"""
        form_data = {
            "titulo": "Tarefa Teste",
            "descricao": "Descrição de teste",
            "data": date.today() + timedelta(days=1),
            "prioridade": "urgente",  # opção inválida
            "categoria": self.categoria.id,
        }
        form = TarefaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("prioridade", form.errors)

    def test_formulario_salvar_tarefa(self):
        """Testa salvamento de tarefa através do formulário"""
        form_data = {
            "titulo": "Tarefa Salva",
            "descricao": "Descrição da tarefa salva",
            "data": date.today() + timedelta(days=2),
            "prioridade": "baixa",
            "categoria": self.categoria.id,
        }
        form = TarefaForm(data=form_data)
        self.assertTrue(form.is_valid())

        tarefa = form.save()
        self.assertEqual(tarefa.titulo, "Tarefa Salva")
        self.assertEqual(tarefa.status, "pendente")  # valor padrão do modelo


class CategoriaFormTests(TestCase):
    def test_formulario_categoria_valido(self):
        """Testa formulário de categoria com dados válidos"""
        form_data = {"nome": "Categoria Teste"}
        form = CategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_categoria_sem_nome(self):
        """Testa formulário sem nome (campo obrigatório)"""
        form_data = {}
        form = CategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

    def test_formulario_categoria_nome_muito_longo(self):
        """Testa formulário com nome muito longo (max 50 caracteres)"""
        nome_longo = "a" * 51  # 51 caracteres
        form_data = {"nome": nome_longo}
        form = CategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

    def test_formulario_categoria_placeholder(self):
        """Testa se o campo nome tem o placeholder correto"""
        form = CategoriaForm()
        placeholder = form.fields["nome"].widget.attrs.get("placeholder")
        self.assertEqual(placeholder, "Digite o nome da categoria")

    def test_formulario_salvar_categoria(self):
        """Testa salvamento de categoria através do formulário"""
        form_data = {"nome": "Categoria Salva"}
        form = CategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())

        categoria = form.save()
        self.assertEqual(categoria.nome, "Categoria Salva")
        self.assertTrue(Categoria.objects.filter(nome="Categoria Salva").exists())


# =============================================
# TESTES EXISTENTES (Listas e Busca)
# =============================================


class ListasBuscaTests(TestCase):
    def setUp(self):
        hoje = date.today()
        amanha = hoje + timedelta(days=1)
        trabalho = Categoria.objects.create(nome="Trabalho")
        lazer = Categoria.objects.create(nome="Lazer")

        Tarefa.objects.create(  # pendente-alta
            titulo="Enviar email urgente",
            descricao="Responder cliente",
            data=amanha,
            prioridade="alta",
            status="pendente",
            categoria=trabalho,
        )

        Tarefa.objects.create(  # pendente-baixa
            titulo="Planejar férias",
            descricao="Ver passagens",
            data=amanha,
            prioridade="baixa",
            status="pendente",
            categoria=lazer,
        )
        Tarefa.objects.create(  # concluída
            titulo="Relatório final",
            descricao="PDF enviado",
            data=hoje,
            prioridade="média",
            status="concluído",
            categoria=trabalho,
        )
        Tarefa.objects.create(  # adiada
            titulo="Comprar presentes",
            descricao="Lembrar de promoções",
            data=hoje,
            prioridade="média",
            status="adiado",
            categoria=lazer,
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
