param(
    [Parameter(Position=0)]
    [string]$Command = "test"
)

# Configurar variables de entorno
$env:PYTHONPATH = "."

Write-Host "=== Ejecutando pruebas ===" -ForegroundColor Green

switch ($Command.ToLower()) {
    "test-service" {
        Write-Host "Ejecutando pruebas del servicio..." -ForegroundColor Yellow
        python -W ignore -m app.tests.test_item_service
    }
    "test-handler" {
        Write-Host "Ejecutando pruebas del handler..." -ForegroundColor Yellow
        python -W ignore -m app.tests.test_item_handlers
    }
    "test-all" {
        Write-Host "Ejecutando todas las pruebas..." -ForegroundColor Yellow
        python -W ignore -m app.tests.test_item_service
        python -W ignore -m app.tests.test_item_handlers
    }
    "test" {
        Write-Host "Ejecutando descubrimiento de pruebas..." -ForegroundColor Yellow
        python -W ignore -m unittest discover app/tests -v
    }
    default {
        Write-Host "Comando no reconocido. Comandos disponibles:" -ForegroundColor Red
        Write-Host "  test-service  - Ejecutar pruebas del servicio" -ForegroundColor Cyan
        Write-Host "  test-handler  - Ejecutar pruebas del handler" -ForegroundColor Cyan
        Write-Host "  test-all      - Ejecutar todas las pruebas" -ForegroundColor Cyan
        Write-Host "  test          - Descubrir y ejecutar todas las pruebas (por defecto)" -ForegroundColor Cyan
    }
} 