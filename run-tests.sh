#!/bin/bash
# Script para executar testes localmente antes do commit/push

echo "🚀 Executando testes do Task Manager..."
echo "=================================="

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ Erro: manage.py não encontrado. Execute este script no diretório raiz do projeto Django."
    exit 1
fi

# Executar verificações do Django
echo "🔍 Verificando configuração do Django..."
python manage.py check
if [ $? -ne 0 ]; then
    echo "❌ Falha na verificação do Django"
    exit 1
fi

# Executar migrações (se necessário)
echo "🗄️ Verificando migrações..."
python manage.py migrate --dry-run > /dev/null 2>&1
if [ $? -eq 0 ]; then
    python manage.py migrate
fi

# Executar testes
echo "🧪 Executando testes da aplicação..."
python manage.py test tarefas --verbosity=2

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Todos os testes passaram com sucesso!"
    echo "🎉 Código está pronto para commit/push"
    echo "=================================="
else
    echo ""
    echo "❌ Alguns testes falharam!"
    echo "🚫 Corrija os problemas antes de fazer commit/push"
    echo "=================================="
    exit 1
fi
