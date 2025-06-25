# 🚀 Configuração de CI/CD para Task Manager

## 📁 Arquivos Criados

### GitHub Actions Workflows
- `.github/workflows/test.yml` - Workflow completo com testes, linting e segurança
- `.github/workflows/pr-quality-check.yml` - Verificação rápida para Pull Requests
- `.github/workflows/README.md` - Documentação dos workflows

### Scripts Locais
- `run-tests.sh` - Script Bash para executar testes localmente (Linux/Mac)
- `run-tests.ps1` - Script PowerShell para executar testes localmente (Windows)

### Configurações
- `.github/branch-protection-config.yml` - Configurações de proteção da branch main
- `.pre-commit-config.yaml` - Configuração para pre-commit hooks
- `requirements-dev.txt` - Dependências de desenvolvimento

## 🛠️ Configuração Inicial

### 1. Instalar Dependências de Desenvolvimento

```bash
# Instalar ferramentas de qualidade de código
pip install -r requirements-dev.txt
```

### 2. Configurar Pre-commit Hooks (Opcional)

```bash
# Instalar pre-commit
pip install pre-commit

# Ativar hooks
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

### 3. Configurar Proteção da Branch Main no GitHub

1. Vá para **Settings** > **Branches** no seu repositório
2. Clique em **Add rule**
3. Configure:
   - Branch name pattern: `main`
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require pull request reviews before merging
   - Status checks obrigatórios:
     - `test (3.11)`
     - `test (3.12)`
     - `lint`
     - `security`
     - `quick-test`

## 🔄 Fluxo de Trabalho

### Para Desenvolvedores

1. **Criar branch para nova funcionalidade:**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. **Desenvolver e escrever testes:**
   - Implementar a funcionalidade
   - Escrever testes correspondentes
   - Seguir padrões de código existentes

3. **Executar testes localmente:**
   ```bash
   # Windows PowerShell
   .\run-tests.ps1
   
   # Linux/Mac Bash
   chmod +x run-tests.sh
   ./run-tests.sh
   ```

4. **Fazer commit e push:**
   ```bash
   git add .
   git commit -m "feat: adicionar nova funcionalidade"
   git push origin feature/nova-funcionalidade
   ```

5. **Criar Pull Request:**
   - Abrir PR no GitHub
   - Aguardar execução automática dos testes
   - Corrigir problemas se necessário
   - Solicitar revisão

6. **Após aprovação, fazer merge**

## 🧪 Testes Automatizados

### O que é testado automaticamente:

#### ✅ Testes Funcionais
- **Modelos:** Criação, validação, relacionamentos
- **Views:** GET/POST, redirecionamentos, context
- **Formulários:** Validação, campos obrigatórios, salvamento
- **Funcionalidades:** Busca, filtros, ordenação

#### ✅ Qualidade de Código
- **Formatação:** Black para formatação consistente
- **Imports:** isort para organização de imports
- **Linting:** flake8 para análise de código
- **Segurança:** safety e bandit para vulnerabilidades

#### ✅ Configuração
- **Django check:** Verificação de configurações
- **Migrações:** Verificação de migrações pendentes
- **Cobertura:** Relatórios de cobertura de testes

## 📊 Relatórios e Artefatos

### Relatórios de Cobertura
- Gerados automaticamente pelo workflow
- Disponíveis como artefatos para download
- Relatório HTML interativo em `htmlcov/`

### Comentários Automáticos no PR
- Status dos testes em tempo real
- Análise de arquivos alterados
- Sugestões de próximos passos

## 🚨 O que Bloqueia o Merge

### ❌ Condições que impedem o merge:
- Testes falhando
- Problemas de linting/formatação
- Vulnerabilidades de segurança detectadas
- Migrações pendentes não aplicadas
- Falta de revisão de código

### ✅ Condições para merge:
- Todos os testes passando
- Código formatado corretamente
- Sem vulnerabilidades críticas
- Aprovação de revisor
- Branch atualizada com main

## 🔧 Resolução de Problemas

### Testes Falhando
```bash
# Executar testes específicos
python manage.py test tarefas.tests.TarefaModelTests -v 2

# Executar com mais detalhes
python manage.py test --verbosity=3 --debug-mode
```

### Problemas de Formatação
```bash
# Corrigir automaticamente
black .
isort .
```

### Problemas de Linting
```bash
# Ver problemas específicos
flake8 . --statistics
```

### Vulnerabilidades de Segurança
```bash
# Verificar dependências
safety check

# Verificar código
bandit -r . -x tests.py,*/migrations/*
```

## 📈 Métricas e Monitoramento

### Métricas Coletadas:
- ✅ Taxa de sucesso dos testes
- ✅ Cobertura de código
- ✅ Tempo de execução dos workflows
- ✅ Frequência de falhas

### Onde Ver:
- **GitHub Actions:** Histórico de execuções
- **Pull Requests:** Comentários automáticos
- **Artefatos:** Relatórios de cobertura

## 🎯 Próximos Passos

1. **Configurar proteção da branch main**
2. **Instalar dependências de desenvolvimento**
3. **Testar o workflow localmente**
4. **Criar primeiro Pull Request**
5. **Configurar notificações (opcional)**
6. **Adicionar mais verificações conforme necessário**

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs do GitHub Actions
2. Executar testes localmente
3. Consultar documentação do projeto
4. Abrir issue no repositório
