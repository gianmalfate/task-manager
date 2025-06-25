# 🧪 Script PowerShell para executar todos os testes localmente
# Executa as mesmas verificações que o CI/CD executa

Write-Host "🚀 Executando verificações de qualidade do código..." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Função para imprimir status
function Print-Status {
    param($ExitCode, $Message)
    if ($ExitCode -eq 0) {
        Write-Host "✅ $Message" -ForegroundColor Green
    } else {
        Write-Host "❌ $Message" -ForegroundColor Red
    }
}

# Função para imprimir informação
function Print-Info {
    param($Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

# Função para imprimir aviso
function Print-Warning {
    param($Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

# Contador de erros
$errors = 0

Write-Host ""
Print-Info "1. Verificando configurações do Django..."
python manage.py check
$checkResult = $LASTEXITCODE
Print-Status $checkResult "Verificação das configurações Django"
if ($checkResult -ne 0) { $errors++ }

Write-Host ""
Print-Info "2. Verificando migrações pendentes..."
python manage.py makemigrations --check --dry-run
$migrationsResult = $LASTEXITCODE
Print-Status $migrationsResult "Verificação de migrações"
if ($migrationsResult -ne 0) { $errors++ }

Write-Host ""
Print-Info "3. Executando migrações..."
python manage.py migrate
$migrateResult = $LASTEXITCODE
Print-Status $migrateResult "Execução das migrações"
if ($migrateResult -ne 0) { $errors++ }

Write-Host ""
Print-Info "4. Executando todos os testes..."
python manage.py test --verbosity=2
$testResult = $LASTEXITCODE
Print-Status $testResult "Execução dos testes"
if ($testResult -ne 0) { $errors++ }

Write-Host ""
Print-Info "5. Executando testes com cobertura..."
if (Get-Command coverage -ErrorAction SilentlyContinue) {
    coverage run --source='.' manage.py test
    $coverageResult = $LASTEXITCODE
    Print-Status $coverageResult "Testes com cobertura"
    if ($coverageResult -eq 0) {
        Write-Host ""
        Print-Info "Relatório de cobertura:"
        coverage report
        coverage html
        Print-Info "Relatório HTML gerado em htmlcov/index.html"
    } else {
        $errors++
    }
} else {
    Print-Warning "Coverage não instalado. Execute: pip install coverage"
}

Write-Host ""
Print-Info "6. Verificando formatação do código..."
if (Get-Command black -ErrorAction SilentlyContinue) {
    black --check --diff .
    $blackResult = $LASTEXITCODE
    Print-Status $blackResult "Formatação com Black"
    if ($blackResult -ne 0) {
        Print-Warning "Execute 'black .' para corrigir a formatação"
        $errors++
    }
} else {
    Print-Warning "Black não instalado. Execute: pip install black"
}

Write-Host ""
Print-Info "7. Verificando ordenação dos imports..."
if (Get-Command isort -ErrorAction SilentlyContinue) {
    isort --check-only --diff .
    $isortResult = $LASTEXITCODE
    Print-Status $isortResult "Ordenação dos imports com isort"
    if ($isortResult -ne 0) {
        Print-Warning "Execute 'isort .' para corrigir a ordenação dos imports"
        $errors++
    }
} else {
    Print-Warning "isort não instalado. Execute: pip install isort"
}

Write-Host ""
Print-Info "8. Análise de código..."
if (Get-Command flake8 -ErrorAction SilentlyContinue) {
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    $flake8Result = $LASTEXITCODE
    Print-Status $flake8Result "Análise de código com flake8"
    if ($flake8Result -ne 0) { $errors++ }
} else {
    Print-Warning "flake8 não instalado. Execute: pip install flake8"
}

Write-Host ""
Print-Info "9. Verificando vulnerabilidades de segurança..."
if (Get-Command safety -ErrorAction SilentlyContinue) {
    safety check
    $safetyResult = $LASTEXITCODE
    Print-Status $safetyResult "Verificação de vulnerabilidades"
    if ($safetyResult -ne 0) { $errors++ }
} else {
    Print-Warning "safety não instalado. Execute: pip install safety"
}

if (Get-Command bandit -ErrorAction SilentlyContinue) {
    bandit -r . -x tests.py,*/migrations/*,*/venv/*,*/.venv/* -f txt
    $banditResult = $LASTEXITCODE
    Print-Status $banditResult "Análise de segurança do código"
    if ($banditResult -ne 0) { $errors++ }
} else {
    Print-Warning "bandit não instalado. Execute: pip install bandit"
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
if ($errors -eq 0) {
    Write-Host "🎉 Todas as verificações passaram!" -ForegroundColor Green
    Write-Host "✅ Seu código está pronto para um Pull Request" -ForegroundColor Green
} else {
    Write-Host "❌ $errors verificação(ões) falharam" -ForegroundColor Red
    Write-Host "🔧 Corrija os problemas antes de criar um PR" -ForegroundColor Red
    exit 1
}

Write-Host ""
Print-Info "Próximos passos:"
Write-Host "1. Git add/commit suas alterações"
Write-Host "2. Git push para sua branch"
Write-Host "3. Crie um Pull Request no GitHub"
Write-Host "4. Aguarde a execução automática dos testes no CI/CD"
