# Configuração do GitHub Actions para Task Manager

## Workflows Criados

### 1. `django-tests.yml` - Workflow Completo
- Executa em múltiplas versões do Python (3.11, 3.12)
- Inclui cache de dependências
- Gera relatório de cobertura opcional
- Mais robusto para projetos grandes

### 2. `ci-simple.yml` - Workflow Simplificado ⭐ **RECOMENDADO**
- Mais rápido e direto
- Focado apenas nos testes essenciais
- Interface mais amigável com emojis
- Ideal para projetos pequenos/médios

## Como Funciona

### Triggers (Quando executa)
- ✅ **Pull Request para main**: Sempre que alguém abrir um PR
- ✅ **Push para main**: Quando código é enviado diretamente para main

### Etapas do CI
1. **Checkout**: Baixa o código do repositório
2. **Setup Python**: Configura ambiente Python 3.12
3. **Instalar deps**: Instala requirements.txt
4. **Check Django**: Verifica configuração
5. **Migrations**: Executa migrações de teste
6. **Run Tests**: Executa os 28 testes criados

### Status do PR
- ❌ **Falha**: PR não pode ser merged
- ✅ **Sucesso**: PR aprovado para merge

## Scripts Locais

### Para Linux/Mac: `run-tests.sh`
```bash
chmod +x run-tests.sh
./run-tests.sh
```

### Para Windows: `run-tests.bat`
```cmd
run-tests.bat
```

## Configuração no GitHub

1. **Push os arquivos** para o repositório
2. **Ativar Actions** (se não estiver ativo)
3. **Configurar Branch Protection** (opcional):
   - Settings → Branches → Add rule
   - Branch name: `main`
   - ✅ Require status checks
   - ✅ Require branches to be up to date
   - Selecionar: "Executar Testes Django"

## Benefícios

### 🛡️ Proteção da Branch Main
- Impede merge de código com testes falhando
- Garante qualidade do código em produção

### 🤖 Automação
- Não precisa lembrar de executar testes manualmente
- Feedback imediato no PR

### 👥 Colaboração
- Outros desenvolvedores veem status dos testes
- Facilita code review

### 📊 Histórico
- Rastreamento de quando testes começaram a falhar
- Relatórios de execução

## Próximos Passos

1. **Escolher workflow**: Recomendo `ci-simple.yml`
2. **Testar**: Fazer um PR de teste
3. **Configurar proteções**: Branch protection rules
4. **Documentar**: Adicionar badge no README

### Badge para README.md
```markdown
![Tests](https://github.com/seu-usuario/task-manager/workflows/CI%20-%20Testes%20Automatizados/badge.svg)
```
