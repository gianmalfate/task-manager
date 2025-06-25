# 🚀 Workflows de CI/CD

Este diretório contém os workflows do GitHub Actions para garantir a qualidade do código do projeto Django Task Manager.

## 📋 Workflows Disponíveis

### 1. **Django Tests** (`test.yml`)
**Executa quando:** Push na main, PRs para main, ou manualmente

**O que faz:**
- 🧪 Executa todos os testes com Python 3.11 e 3.12
- 📊 Gera relatórios de cobertura de código
- 🔍 Faz linting com Black, isort e flake8
- 🛡️ Verifica vulnerabilidades de segurança
- ✅ Confirma que o código está pronto para produção

### 2. **PR Quality Check** (`pr-quality-check.yml`)
**Executa quando:** PR é aberto/atualizado para main

**O que faz:**
- ⚡ Testes rápidos focados no PR
- 💬 Comenta automaticamente o resultado no PR
- 📁 Analisa quais arquivos foram alterados
- ⚠️ Alerta sobre possíveis impactos nos testes

## 🧪 Testes Executados

### Modelos (`TarefaModelTests`, `CategoriaModelTests`)
- ✅ Criação de objetos com todos os campos
- ✅ Valores padrão dos campos
- ✅ Validação de opções (prioridade, status)
- ✅ Relacionamentos entre modelos
- ✅ Métodos `__str__`

### Views (`TarefaViewTests`)
- ✅ Carregamento de páginas (GET)
- ✅ Criação de tarefas (POST)
- ✅ Operações CRUD (criar, ler, atualizar, deletar)
- ✅ Redirecionamentos corretos
- ✅ Context data das views

### Formulários (`TarefaFormTests`, `CategoriaFormTests`)
- ✅ Validação de dados válidos/inválidos
- ✅ Campos obrigatórios
- ✅ Widgets personalizados
- ✅ Limites de tamanho
- ✅ Salvamento através do formulário

### Funcionalidades (`ListasBuscaTests`)
- ✅ Busca por termos
- ✅ Filtros por categoria
- ✅ Ordenação por prioridade
- ✅ Paginação e resultados vazios

## 📊 Relatórios de Cobertura

Os workflows geram relatórios de cobertura que podem ser baixados como artefatos do GitHub Actions. Estes relatórios mostram:

- **Linhas cobertas/não cobertas** por testes
- **Percentual de cobertura** por arquivo
- **Relatório HTML** interativo para análise detalhada

## 🛡️ Proteção da Branch Main

Para configurar a proteção da branch main no GitHub:

1. Vá para **Settings** > **Branches**
2. Clique em **Add rule** ou edite a regra existente
3. Configure:
   - Branch name pattern: `main`
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require pull request reviews before merging
   - ❌ Allow force pushes
   - ❌ Allow deletions

### Status Checks Obrigatórios:
- `test (3.11)` - Testes com Python 3.11
- `test (3.12)` - Testes com Python 3.12
- `lint` - Verificação de linting
- `security` - Verificação de segurança
- `quick-test` - Testes rápidos do PR

## 🔧 Configuração Local

Para executar as mesmas verificações localmente:

```bash
# Instalar dependências de desenvolvimento
pip install black isort flake8 coverage safety bandit

# Executar testes
python manage.py test --verbosity=2

# Executar com cobertura
coverage run --source='.' manage.py test
coverage report
coverage html

# Formatação de código
black .
isort .

# Linting
flake8 .

# Verificações de segurança
safety check
bandit -r . -x tests.py,*/migrations/*
```

## 🚀 Fluxo de Trabalho

1. **Desenvolver** nova funcionalidade em branch separada
2. **Escrever testes** para a nova funcionalidade
3. **Executar testes localmente** para verificar
4. **Criar Pull Request** para main
5. **Aguardar** execução automática dos workflows
6. **Corrigir** eventuais problemas apontados
7. **Solicitar revisão** do código
8. **Fazer merge** após aprovação e testes passando

## 📝 Adicionando Novos Testes

Ao adicionar novos testes, certifique-se de:

- ✅ Seguir o padrão de nomenclatura existente
- ✅ Incluir docstrings explicativas
- ✅ Testar casos válidos e inválidos
- ✅ Verificar se os testes passam localmente
- ✅ Manter boa cobertura de código

## 🤝 Contribuindo

Antes de criar um PR:

1. Certifique-se de que todos os testes passam
2. Adicione testes para novas funcionalidades
3. Mantenha a cobertura de código alta
4. Siga as convenções de código do projeto
5. Atualize a documentação se necessário

## 📞 Suporte

Se encontrar problemas com os workflows:

1. Verifique os logs do GitHub Actions
2. Execute os testes localmente
3. Consulte a documentação do Django
4. Abra uma issue descrevendo o problema
