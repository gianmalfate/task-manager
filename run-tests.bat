@echo off
REM Script para executar testes localmente no Windows

echo 🚀 Executando testes do Task Manager...
echo ==================================

REM Verificar se estamos no diretório correto
if not exist "manage.py" (
    echo ❌ Erro: manage.py não encontrado. Execute este script no diretório raiz do projeto Django.
    exit /b 1
)

REM Executar verificações do Django
echo 🔍 Verificando configuração do Django...
python manage.py check
if %errorlevel% neq 0 (
    echo ❌ Falha na verificação do Django
    exit /b 1
)

REM Executar migrações (se necessário)
echo 🗄️ Executando migrações...
python manage.py migrate

REM Executar testes
echo 🧪 Executando testes da aplicação...
python manage.py test tarefas --verbosity=2

if %errorlevel% equ 0 (
    echo.
    echo ✅ Todos os testes passaram com sucesso!
    echo 🎉 Código está pronto para commit/push
    echo ==================================
) else (
    echo.
    echo ❌ Alguns testes falharam!
    echo 🚫 Corrija os problemas antes de fazer commit/push
    echo ==================================
    exit /b 1
)
