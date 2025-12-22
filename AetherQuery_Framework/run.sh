#!/bin/bash
# run.sh

echo "🚀 Запуск Aether Query Server..."

# Сборка
echo "🔨 Сборка сервера..."
go build -o aether_query cmd/server/main.go

# Проверка
if [ ! -f "aether_query" ]; then
    echo "❌ Ошибка сборки сервера"
    exit 1
fi

echo "✅ Сервер собран успешно"
echo ""
echo "✨ Aether Query Server"
echo "📡 Адрес: http://localhost:8080"
echo "📊 Эндпоинты:"
echo "  GET  /                 - Информация о сервере"
echo "  GET  /health           - Проверка здоровья"
echo "  POST /query            - Выполнение запроса"
echo "  GET  /query/examples   - Примеры запросов"
echo "  GET  /clients          - Список клиентов"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

# Запуск
./aether_query