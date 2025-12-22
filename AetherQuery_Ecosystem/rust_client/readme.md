AetherQuery Rust Client

Простой, но мощный CLI-клиент для AetherQuery сервера.

## Установка

```bash
git clone <репозиторий>
cd rust_client
cargo build --release
Использование
Базовые команды:
bash
# Проверить статус сервера
./target/release/aether-cli status

# Выполнить SQL запрос
./target/release/aether-cli query "SELECT * FROM users"

# Интерактивный режим
./target/release/aether-cli shell

# Список таблиц
./target/release/aether-cli tables

# Описание таблицы
./target/release/aether-cli describe users
Опции:
bash
# Указать сервер
./target/release/aether-cli --server http://localhost:8080 status

# Изменить формат вывода
./target/release/aether-cli --format json query "SELECT 1"

# Включить подробный вывод
./target/release/aether-cli --verbose status

# Сохранить результаты в файл
./target/release/aether-cli query "SELECT * FROM logs" --output results.json
Переменные окружения
bash
export AETHER_SERVER="http://localhost:8080"
Интерактивный режим
В интерактивном режиме доступны специальные команды:

\?, \h - помощь

\q, \quit - выход

\t - список таблиц

\d таблица - описание таблицы

\s - статус сервера

\f формат - изменить формат вывода

text

### 2. Создаем файл конфигурации `.env.example`:
AETHER_SERVER=http://localhost:8080

text

### 3. Добавим полезные скрипты:

`scripts/test_all.sh`:
```bash
#!/bin/bash

echo "=== Полное тестирование AetherQuery CLI ==="

# Тест 1: Помощь
echo "1. Тестируем --help"
cargo run -- --help

# Тест 2: Статус сервера
echo -e "\n2. Проверяем статус сервера"
cargo run -- status

# Тест 3: Разные форматы вывода
echo -e "\n3. Тестируем форматы вывода"
for format in table json csv markdown raw; do
    echo "Формат: $format"
    cargo run -- --format $format query "SELECT 1" 2>/dev/null || true
done

# Тест 4: Verbose режим
echo -e "\n4. Verbose режим"
cargo run -- --verbose status

# Тест 5: Сохранение в файл
echo -e "\n5. Сохранение результатов в файл"
cargo run -- query "SELECT 1" --output /tmp/test_output.txt
cat /tmp/test_output.txt

echo -e "\n=== Тестирование завершено ==="