
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Tarefa, Categoria
from .forms import TarefaForm, CategoriaForm


class CategoriaModelTest(TestCase):
    """Testes para o modelo Categoria"""
    
    def test_criacao_categoria(self):
        """Testa a criação de uma categoria"""
        categoria = Categoria.objects.create(nome="Trabalho")
        self.assertEqual(categoria.nome, "Trabalho")
        self.assertEqual(str(categoria), "Trabalho")
    
    def test_categoria_default(self):
        """Testa se o valor padrão da categoria é 'Geral'"""
        categoria = Categoria.objects.create()
        self.assertEqual(categoria.nome, "Geral")


class TarefaModelTest(TestCase):
    """Testes para o modelo Tarefa"""
    
    def setUp(self):
        """Configura dados iniciais para os testes"""
        self.categoria = Categoria.objects.create(nome="Pessoal")
    
    def test_criacao_tarefa(self):
        """Testa a criação de uma tarefa"""
        tarefa = Tarefa.objects.create(
            titulo="Estudar Django",
            descricao="Estudar testes em Django",
            data=date.today(),
            prioridade="alta",
            status="pendente",
            categoria=self.categoria
        )
        
        self.assertEqual(tarefa.titulo, "Estudar Django")
        self.assertEqual(tarefa.descricao, "Estudar testes em Django")
        self.assertEqual(tarefa.data, date.today())
        self.assertEqual(tarefa.prioridade, "alta")
        self.assertEqual(tarefa.status, "pendente")
        self.assertEqual(tarefa.categoria, self.categoria)
        self.assertEqual(str(tarefa), "Estudar Django")
    
    def test_tarefa_defaults(self):
        """Testa os valores padrão de uma tarefa"""
        tarefa = Tarefa.objects.create(
            descricao="Tarefa de teste",
            data=date.today(),
            categoria=self.categoria
        )
        
        self.assertEqual(tarefa.titulo, "Sem título")
        self.assertEqual(tarefa.prioridade, "média")
        self.assertEqual(tarefa.status, "pendente")
    
    def test_opcoes_prioridade(self):
        """Testa se as opções de prioridade estão funcionando"""
        opcoes_prioridade = ["alta", "média", "baixa"]
        
        for prioridade in opcoes_prioridade:
            tarefa = Tarefa.objects.create(
                descricao=f"Teste prioridade {prioridade}",
                data=date.today(),
                prioridade=prioridade,
                categoria=self.categoria
            )
            self.assertEqual(tarefa.prioridade, prioridade)
    
    def test_opcoes_status(self):
        """Testa se as opções de status estão funcionando"""
        opcoes_status = ["concluído", "pendente", "adiado"]
        
        for status in opcoes_status:
            tarefa = Tarefa.objects.create(
                descricao=f"Teste status {status}",
                data=date.today(),
                status=status,
                categoria=self.categoria
            )
            self.assertEqual(tarefa.status, status)
    
    def test_relacionamento_categoria(self):
        """Testa o relacionamento entre Tarefa e Categoria"""
        tarefa = Tarefa.objects.create(
            titulo="Tarefa relacionada",
            descricao="Teste de relacionamento",
            data=date.today(),
            categoria=self.categoria
        )
        
        # Testa se a tarefa está relacionada à categoria
        self.assertEqual(tarefa.categoria, self.categoria)
        
        # Testa se a categoria tem a tarefa no related_name
        self.assertIn(tarefa, self.categoria.tarefas.all())


class TarefaViewsTest(TestCase):
    """Testes para as views de Tarefa"""
    
    def setUp(self):
        """Configura dados iniciais para os testes"""
        self.client = Client()
        self.categoria = Categoria.objects.create(nome="Teste")
        self.tarefa_pendente = Tarefa.objects.create(
            titulo="Tarefa Pendente",
            descricao="Descrição da tarefa pendente",
            data=date.today(),
            prioridade="alta",
            status="pendente",
            categoria=self.categoria
        )
        self.tarefa_concluida = Tarefa.objects.create(
            titulo="Tarefa Concluída",
            descricao="Descrição da tarefa concluída",
            data=date.today(),
            prioridade="baixa",
            status="concluído",
            categoria=self.categoria
        )
    
    def test_lista_tarefas_pendentes_view(self):
        """Testa o carregamento da lista de tarefas pendentes"""
        url = reverse('tarefas_pendentes_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarefa Pendente")
        self.assertNotContains(response, "Tarefa Concluída")
        self.assertIn('tarefas_pendentes', response.context)
        self.assertEqual(len(response.context['tarefas_pendentes']), 1)
    
    def test_lista_tarefas_com_busca(self):
        """Testa a funcionalidade de busca na lista de tarefas"""
        url = reverse('tarefas_pendentes_list')
        response = self.client.get(url, {'q': 'Pendente'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tarefa Pendente")
        self.assertEqual(len(response.context['tarefas_pendentes']), 1)
        
        # Testa busca que não encontra nada
        response = self.client.get(url, {'q': 'Inexistente'})
        self.assertEqual(len(response.context['tarefas_pendentes']), 0)
    
    def test_lista_tarefas_filtro_categoria(self):
        """Testa o filtro por categoria"""
        categoria2 = Categoria.objects.create(nome="Trabalho")
        Tarefa.objects.create(
            titulo="Tarefa Trabalho",
            descricao="Tarefa de trabalho",
            data=date.today(),
            categoria=categoria2
        )
        
        url = reverse('tarefas_pendentes_list')
        response = self.client.get(url, {'categoria': self.categoria.id})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tarefas_pendentes']), 1)
        self.assertContains(response, "Tarefa Pendente")
        self.assertNotContains(response, "Tarefa Trabalho")
    
    def test_adicionar_tarefa_get(self):
        """Testa o carregamento da página de adicionar tarefa"""
        url = reverse('adicionar_tarefa')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], TarefaForm)
    
    def test_adicionar_tarefa_post_valido(self):
        """Testa a criação de uma tarefa via POST"""
        url = reverse('adicionar_tarefa')
        data = {
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da nova tarefa',
            'data': date.today().strftime('%Y-%m-%d'),
            'prioridade': 'média',
            'categoria': self.categoria.id
        }
        
        response = self.client.post(url, data)
        
        # Deve redirecionar após criação bem-sucedida
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tarefas_pendentes_list'))
        
        # Verifica se a tarefa foi criada
        self.assertTrue(Tarefa.objects.filter(titulo='Nova Tarefa').exists())
    
    def test_concluir_tarefa(self):
        """Testa a conclusão de uma tarefa"""
        url = reverse('concluir_tarefa', kwargs={'tarefa_id': self.tarefa_pendente.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tarefas_pendentes_list'))
        
        # Verifica se o status foi alterado
        self.tarefa_pendente.refresh_from_db()
        self.assertEqual(self.tarefa_pendente.status, 'concluído')
    
    def test_excluir_tarefa(self):
        """Testa a exclusão de uma tarefa"""
        tarefa_id = self.tarefa_pendente.id
        url = reverse('excluir_tarefa', kwargs={'tarefa_id': tarefa_id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tarefas_pendentes_list'))
        
        # Verifica se a tarefa foi excluída
        self.assertFalse(Tarefa.objects.filter(id=tarefa_id).exists())
    
    def test_adiar_tarefa(self):
        """Testa o adiamento de uma tarefa"""
        url = reverse('adiar_tarefa', kwargs={'tarefa_id': self.tarefa_pendente.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tarefas_pendentes_list'))
        
        # Verifica se o status foi alterado
        self.tarefa_pendente.refresh_from_db()
        self.assertEqual(self.tarefa_pendente.status, 'adiado')


class TarefaFormTest(TestCase):
    """Testes para o formulário de Tarefa"""
    
    def setUp(self):
        """Configura dados iniciais para os testes"""
        self.categoria = Categoria.objects.create(nome="Teste")
    
    def test_formulario_valido(self):
        """Testa um formulário válido"""
        form_data = {
            'titulo': 'Tarefa de Teste',
            'descricao': 'Descrição da tarefa de teste',
            'data': date.today().strftime('%Y-%m-%d'),
            'prioridade': 'alta',
            'categoria': self.categoria.id
        }
        
        form = TarefaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formulario_campos_obrigatorios(self):
        """Testa se os campos obrigatórios são validados"""
        form_data = {}
        form = TarefaForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('descricao', form.errors)
        self.assertIn('data', form.errors)
        self.assertIn('categoria', form.errors)
    
    def test_formulario_data_passada(self):
        """Testa se o formulário aceita datas válidas"""
        form_data = {
            'titulo': 'Tarefa de Teste',
            'descricao': 'Descrição da tarefa de teste',
            'data': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'prioridade': 'alta',
            'categoria': self.categoria.id
        }
        
        form = TarefaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formulario_prioridade_choices(self):
        """Testa se as opções de prioridade estão corretas"""
        form_data = {
            'titulo': 'Tarefa de Teste',
            'descricao': 'Descrição da tarefa de teste',
            'data': date.today().strftime('%Y-%m-%d'),
            'prioridade': 'prioridade_inexistente',
            'categoria': self.categoria.id
        }
        
        form = TarefaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prioridade', form.errors)
    
    def test_formulario_save(self):
        """Testa se o formulário salva corretamente"""
        form_data = {
            'titulo': 'Tarefa Salva',
            'descricao': 'Descrição da tarefa salva',
            'data': date.today().strftime('%Y-%m-%d'),
            'prioridade': 'baixa',
            'categoria': self.categoria.id
        }
        
        form = TarefaForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        tarefa = form.save()
        self.assertIsInstance(tarefa, Tarefa)
        self.assertEqual(tarefa.titulo, 'Tarefa Salva')
        self.assertEqual(tarefa.descricao, 'Descrição da tarefa salva')
        self.assertEqual(tarefa.prioridade, 'baixa')
        self.assertEqual(tarefa.categoria, self.categoria)


class CategoriaFormTest(TestCase):
    """Testes para o formulário de Categoria"""
    
    def test_formulario_categoria_valido(self):
        """Testa um formulário de categoria válido"""
        form_data = {'nome': 'Nova Categoria'}
        form = CategoriaForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_formulario_categoria_campo_obrigatorio(self):
        """Testa se o campo nome é obrigatório"""
        form_data = {'nome': ''}
        form = CategoriaForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
    
    def test_formulario_categoria_save(self):
        """Testa se o formulário de categoria salva corretamente"""
        form_data = {'nome': 'Categoria Salva'}
        form = CategoriaForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        categoria = form.save()
        
        self.assertIsInstance(categoria, Categoria)
        self.assertEqual(categoria.nome, 'Categoria Salva')


class IntegrationTest(TestCase):
    """Testes de integração"""
    
    def setUp(self):
        """Configura dados iniciais para os testes"""
        self.client = Client()
        self.categoria = Categoria.objects.create(nome="Integração")
    
    def test_fluxo_completo_tarefa(self):
        """Testa o fluxo completo de criação, edição e conclusão de tarefa"""
        # 1. Criar tarefa
        url_criar = reverse('adicionar_tarefa')
        data_criar = {
            'titulo': 'Tarefa Integração',
            'descricao': 'Teste de integração completo',
            'data': date.today().strftime('%Y-%m-%d'),
            'prioridade': 'alta',
            'categoria': self.categoria.id
        }
        
        response = self.client.post(url_criar, data_criar)
        self.assertEqual(response.status_code, 302)
        
        # Verifica se a tarefa foi criada
        tarefa = Tarefa.objects.get(titulo='Tarefa Integração')
        self.assertEqual(tarefa.status, 'pendente')
        
        # 2. Verificar se aparece na lista
        url_lista = reverse('tarefas_pendentes_list')
        response = self.client.get(url_lista)
        self.assertContains(response, 'Tarefa Integração')
        
        # 3. Concluir tarefa
        url_concluir = reverse('concluir_tarefa', kwargs={'tarefa_id': tarefa.id})
        response = self.client.get(url_concluir)
        self.assertEqual(response.status_code, 302)
        
        # 4. Verificar se não aparece mais na lista de pendentes
        response = self.client.get(url_lista)
        self.assertNotContains(response, 'Tarefa Integração')
        
        # 5. Verificar se o status foi alterado
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.status, 'concluído')


# Testes das funcionalidades existentes (buscas e filtros)
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

    # 2 ─ Filtro por categoria em pendentes
    def test_filtro_categoria(self):
        lazer = Categoria.objects.get(nome="Lazer").id
        url = reverse("tarefas_pendentes_list") + f"?categoria={lazer}"
        resp = self.client.get(url)
        self.assertContains(resp, "Planejar férias")
        self.assertNotContains(resp, "Enviar email urgente")

    # 3 ─ Ordenação por prioridade (alta deve vir antes de baixa)
    def test_ordenar_por_prioridade(self):
        url = reverse("tarefas_pendentes_list") + "?ordenar_por=prioridade"
        resp = self.client.get(url)
        tarefas = list(resp.context["tarefas_pendentes"])
        self.assertEqual(tarefas[0].prioridade, "alta")
        self.assertEqual(tarefas[1].prioridade, "baixa")

    # 4 ─ Busca vazia devolve todas as pendentes
    def test_busca_vazia(self):
        url = reverse("tarefas_pendentes_list")  # sem q=
        resp = self.client.get(url)
        self.assertEqual(resp.context["tarefas_pendentes"].count(), 2)