#!/bin/bash

# 🧪 Script para executar todos os testes localmente
# Executa as mesmas verificações que o CI/CD executa

echo "🚀 Executando verificações de qualidade do código..."
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Função para imprimir informação
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Função para imprimir aviso
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Contador de erros
errors=0

echo ""
print_info "1. Verificando configurações do Django..."
python manage.py check
check_result=$?
print_status $check_result "Verificação das configurações Django"
if [ $check_result -ne 0 ]; then ((errors++)); fi

echo ""
print_info "2. Verificando migrações pendentes..."
python manage.py makemigrations --check --dry-run
migrations_result=$?
print_status $migrations_result "Verificação de migrações"
if [ $migrations_result -ne 0 ]; then ((errors++)); fi

echo ""
print_info "3. Executando migrações..."
python manage.py migrate
migrate_result=$?
print_status $migrate_result "Execução das migrações"
if [ $migrate_result -ne 0 ]; then ((errors++)); fi

echo ""
print_info "4. Executando todos os testes..."
python manage.py test --verbosity=2
test_result=$?
print_status $test_result "Execução dos testes"
if [ $test_result -ne 0 ]; then ((errors++)); fi

echo ""
print_info "5. Executando testes com cobertura..."
if command -v coverage &> /dev/null; then
    coverage run --source='.' manage.py test
    coverage_result=$?
    print_status $coverage_result "Testes com cobertura"
    if [ $coverage_result -eq 0 ]; then
        echo ""
        print_info "Relatório de cobertura:"
        coverage report
        coverage html
        print_info "Relatório HTML gerado em htmlcov/index.html"
    else
        ((errors++))
    fi
else
    print_warning "Coverage não instalado. Execute: pip install coverage"
fi

echo ""
print_info "6. Verificando formatação do código..."
if command -v black &> /dev/null; then
    black --check --diff .
    black_result=$?
    print_status $black_result "Formatação com Black"
    if [ $black_result -ne 0 ]; then
        print_warning "Execute 'black .' para corrigir a formatação"
        ((errors++))
    fi
else
    print_warning "Black não instalado. Execute: pip install black"
fi

echo ""
print_info "7. Verificando ordenação dos imports..."
if command -v isort &> /dev/null; then
    isort --check-only --diff .
    isort_result=$?
    print_status $isort_result "Ordenação dos imports com isort"
    if [ $isort_result -ne 0 ]; then
        print_warning "Execute 'isort .' para corrigir a ordenação dos imports"
        ((errors++))
    fi
else
    print_warning "isort não instalado. Execute: pip install isort"
fi

echo ""
print_info "8. Análise de código..."
if command -v flake8 &> /dev/null; then
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8_result=$?
    print_status $flake8_result "Análise de código com flake8"
    if [ $flake8_result -ne 0 ]; then ((errors++)); fi
else
    print_warning "flake8 não instalado. Execute: pip install flake8"
fi

echo ""
print_info "9. Verificando vulnerabilidades de segurança..."
if command -v safety &> /dev/null; then
    safety check
    safety_result=$?
    print_status $safety_result "Verificação de vulnerabilidades"
    if [ $safety_result -ne 0 ]; then ((errors++)); fi
else
    print_warning "safety não instalado. Execute: pip install safety"
fi

if command -v bandit &> /dev/null; then
    bandit -r . -x tests.py,*/migrations/*,*/venv/*,*/.venv/* -f txt
    bandit_result=$?
    print_status $bandit_result "Análise de segurança do código"
    if [ $bandit_result -ne 0 ]; then ((errors++)); fi
else
    print_warning "bandit não instalado. Execute: pip install bandit"
fi

echo ""
echo "=================================================="
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}🎉 Todas as verificações passaram!${NC}"
    echo -e "${GREEN}✅ Seu código está pronto para um Pull Request${NC}"
else
    echo -e "${RED}❌ $errors verificação(ões) falharam${NC}"
    echo -e "${RED}🔧 Corrija os problemas antes de criar um PR${NC}"
    exit 1
fi

echo ""
print_info "Próximos passos:"
echo "1. Git add/commit suas alterações"
echo "2. Git push para sua branch"
echo "3. Crie um Pull Request no GitHub"
echo "4. Aguarde a execução automática dos testes no CI/CD"
