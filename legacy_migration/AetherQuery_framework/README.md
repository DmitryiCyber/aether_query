AetherQuery Framework
<div align="center">
🚀 Универсальный мультиязычный фреймворк для работы с базами данных

https://img.shields.io/badge/python-3.10+-blue.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/code%2520style-black-000000.svg

Единый API для 5 языков программирования и 5 типов баз данных

</div>
📖 Оглавление
🌟 Особенности

🛠 Поддерживаемые технологии

🚀 Быстрый старт

💡 Примеры использования

🗃 Поддерживаемые базы данных

🌍 Мультиязычная архитектура

📦 Установка

🔧 Конфигурация

🧪 Тестирование

🤝 Вклад в проект

📄 Лицензия

🌟 Особенности
🎯 Единый API
Унифицированный интерфейс для всех поддерживаемых БД

Идентичные методы во всех языковых реализациях

Автоматическое определение типа базы данных

🔄 Кросс-платформенность
Нативная поддержка Windows, Linux, macOS

Docker-контейнеры для изоляции зависимостей

Cloud-ready архитектура

🛡 Безопасность и надежность
Защита от SQL-инъекций

Подготовленные statements

Автоматическое управление соединениями

Расширенная обработка ошибок

⚡ Производительность
Connection pooling

Асинхронная поддержка

Кэширование запросов

Оптимизированные драйверы

🛠 Поддерживаемые технологии
🗃 Базы данных
База данных	Тип	Статус	Особенности
PostgreSQL	Реляционная	✅ Готов	Расширения, JSONB, полнотекстовый поиск
MySQL	Реляционная	✅ Готов	Репликация, кластеризация
SQLite	Встроенная	✅ Готов	Zero-configuration, embedded
MongoDB	Документная	✅ Готов	Aggregation pipeline, GridFS
Redis	Key-Value	✅ Готов	Кэширование, pub/sub, геоданные
💻 Языки программирования
Язык	Статус	Целевое использование
Python	✅ Готов	Data science, ML, веб-приложения
Go	🚧 В разработке	Высоконагруженные системы
Rust	🚧 В разработке	Системное программирование
TypeScript	🚧 В разработке	Веб-приложения, Node.js
C#	🚧 В разработке	Enterprise, игры, Windows
🚀 Быстрый старт
Установка (Python)
bash
# Клонирование репозитория
git clone https://github.com/aetherquery/aetherquery-framework.git
cd aetherquery-framework

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Установка фреймворка
pip install -e .
Базовое использование
python
from aetherquery import DatabaseConnection
from aetherquery.core.config import DatabaseConfig

# Конфигурация PostgreSQL
config = DatabaseConfig(
    type="postgresql",
    host="localhost",
    port=5432,
    username="user",
    password="pass",
    database="myapp"
)

# Использование контекстного менеджера
with DatabaseConnection(config) as db:
    # Создание таблицы
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE
        )
    """)
    
    # Вставка данных
    db.execute(
        "INSERT INTO users (name, email) VALUES (%(name)s, %(email)s)",
        {"name": "Alice", "email": "alice@example.com"}
    )
    
    # Чтение данных
    result = db.execute("SELECT * FROM users")
    
    # Преобразование в словари
    users = result.to_dict()
    for user in users:
        print(f"User: {user['name']} - {user['email']}")
💡 Примеры использования
Работа с транзакциями
python
with DatabaseConnection(config) as db:
    # Начало транзакции
    db.execute("BEGIN")
    
    try:
        # Несколько операций
        db.execute("INSERT INTO accounts (user_id, balance) VALUES (1, 1000)")
        db.execute("INSERT INTO transactions (account_id, amount) VALUES (1, 1000)")
        
        # Коммит транзакции
        db.execute("COMMIT")
        print("✅ Транзакция завершена успешно")
        
    except Exception as e:
        # Откат при ошибке
        db.execute("ROLLBACK")
        print(f"❌ Транзакция откатана: {e}")
Работа с MongoDB
python
# Конфигурация MongoDB
mongo_config = DatabaseConfig(
    type="mongodb",
    host="localhost",
    port=27017,
    database="myapp"
)

with DatabaseConnection(mongo_config) as db:
    # Вставка документов
    db.execute(
        "db.users.insert",
        {"documents": [
            {"name": "Bob", "age": 25, "interests": ["music", "sports"]},
            {"name": "Charlie", "age": 30, "interests": ["reading", "travel"]}
        ]}
    )
    
    # Поиск документов
    result = db.execute(
        "db.users.find",
        {"filter": {"age": {"$gt": 25}}}
    )
Работа с Redis
python
# Конфигурация Redis
redis_config = DatabaseConfig(
    type="redis",
    host="localhost",
    port=6379,
    database="0"
)

with DatabaseConnection(redis_config) as db:
    # Кэширование данных
    db.execute("SET user:1:name 'Alice'")
    db.execute("EXPIRE user:1:name 3600")  # TTL 1 час
    
    # Чтение из кэша
    result = db.execute("GET user:1:name")
    if result.rows:
        print(f"Username: {result.rows[0][0]}")
🗃 Поддерживаемые базы данных
PostgreSQL
python
config = DatabaseConfig(
    type="postgresql",
    host="localhost",
    username="user",
    password="pass",
    database="app_db",
    ssl=True
)
MySQL
python
config = DatabaseConfig(
    type="mysql", 
    host="localhost",
    username="root",
    password="password",
    database="app_db"
)
SQLite
python
config = DatabaseConfig(
    type="sqlite",
    path="/path/to/database.db"  # или ":memory:" для in-memory БД
)
MongoDB
python
config = DatabaseConfig(
    type="mongodb",
    host="localhost",
    database="app_db"
)
Redis
python
config = DatabaseConfig(
    type="redis",
    host="localhost",
    database="0"  # номер БД Redis
)
🌍 Мультиязычная архитектура
Python (референсная реализация)
python
# Установка
pip install aetherquery-python

# Использование
from aetherquery_python import DatabaseConnection
Go (в разработке)
go
// Установка
go get github.com/aetherquery/aetherquery-go

// Использование
import "github.com/aetherquery/aetherquery-go"

conn := aetherquery.NewConnection(config)
result, err := conn.Query("SELECT * FROM users")
Rust (в разработке)
rust
// Cargo.toml
[dependencies]
aetherquery = "0.1.0"

// Использование
use aetherquery::DatabaseConnection;

let conn = DatabaseConnection::new(config);
let result = conn.execute("SELECT * FROM users").await?;
TypeScript (в разработке)
typescript
// Установка
npm install aetherquery

// Использование
import { DatabaseConnection } from 'aetherquery';

const conn = new DatabaseConnection(config);
const result = await conn.query('SELECT * FROM users');
C# (в разработке)
csharp
// Установка
dotnet add package AetherQuery

// Использование
using AetherQuery;

var conn = new DatabaseConnection(config);
var result = conn.Execute("SELECT * FROM users");
📦 Установка
Полная установка (все зависимости)
bash
pip install -e ".[all]"
Минимальная установка
bash
pip install -e .
Установка с конкретными адаптерами
bash
# Только PostgreSQL
pip install -e ".[postgresql]"

# PostgreSQL + Redis
pip install -e ".[postgresql,redis]"

# Для разработки
pip install -e ".[dev]"
🔧 Конфигурация
Конфигурационный файл
Создайте config.yaml:

yaml
database:
  type: "postgresql"
  host: "localhost"
  port: 5432
  username: "${DB_USER}"
  password: "${DB_PASS}"
  database: "myapp"
  ssl: true

logging:
  level: "INFO"
  format: "json"

performance:
  pool_size: 10
  timeout: 30
  max_query_size: 1048576
Переменные окружения
bash
export AETHERQUERY_DB_TYPE="postgresql"
export AETHERQUERY_DB_HOST="localhost"
export AETHERQUERY_DB_USERNAME="user"
export AETHERQUERY_DB_PASSWORD="pass"
Программная конфигурация
python
from aetherquery.core.config import DatabaseConfig, AetherQueryConfig

config = AetherQueryConfig(
    database=DatabaseConfig(
        type="postgresql",
        host="localhost",
        username="user",
        password="pass",
        database="myapp"
    ),
    log_level="INFO",
    max_query_size=1024*1024
)
🧪 Тестирование
Запуск тестов
bash
# Все тесты
pytest tests/ -v

# Конкретный адаптер
pytest tests/test_postgresql_adapter.py -v

# С покрытием кода
pytest tests/ --cov=src/aetherquery --cov-report=html
Тестирование с Docker
bash
# Запуск тестовых БД
docker-compose -f docker-compose.test.yml up -d

# Запуск тестов
./scripts/run_tests_with_docker.sh
Тестовые конфигурации
python
# Тестирование с SQLite in-memory
test_config = DatabaseConfig(type="sqlite", path=":memory:")

# Тестирование с конкретной БД
test_config = DatabaseConfig(
    type="postgresql",
    host="localhost",
    database="test_db"
)
🏗 Архитектура
text
aetherquery-framework/
├── src/
│   └── aetherquery/
│       ├── core/                 # Общее ядро
│       │   ├── interfaces.py     # Базовые интерфейсы
│       │   ├── config.py         # Конфигурация
│       │   └── exceptions.py     # Система исключений
│       ├── db/                   # Работа с БД
│       │   ├── adapters/         # Адаптеры БД
│       │   │   ├── postgresql.py
│       │   │   ├── mysql.py
│       │   │   ├── sqlite.py
│       │   │   ├── mongodb.py
│       │   │   └── redis.py
│       │   └── connection.py     # Менеджер соединений
│       └── types/               # Типы данных
├── tests/                       # Тесты
├── examples/                    # Примеры использования
└── docs/                        # Документация
🤝 Вклад в проект
Мы приветствуем вклад в развитие AetherQuery!

Как помочь:
Сообщения об ошибках: Используйте GitHub Issues

Новые функции: Создайте Feature Request

Код: Сделайте Pull Request

Документация: Помогите улучшить документацию

Тестирование: Протестируйте на разных окружениях

Процесс разработки:
bash
# Форк репозитория
git clone https://github.com/your-username/aetherquery-framework.git

# Создание ветки для фичи
git checkout -b feature/amazing-feature

# Установка для разработки
pip install -e ".[dev]"

# Запуск тестов
pytest tests/

# Форматирование кода
black src/ tests/
ruff check src/ tests/
Руководство по коду:
Следуйте PEP 8 (Python)

Используйте type hints

Пишите документацию для всех публичных методов

Добавляйте тесты для новой функциональности

📄 Лицензия
Этот проект распространяется под лицензией MIT. Смотрите файл LICENSE для подробностей.

🔮 Дорожная карта
Версия 1.0 (Текущая)
✅ Поддержка 5 типов БД на Python

✅ Базовые операции CRUD

✅ Система конфигурации

✅ Комплексное тестирование

Версия 1.1 (Планируется)
🚧 Connection pooling

🚧 Расширенная система транзакций

🚧 Query Builder

🚧 Система миграций

Версия 2.0 (Будущее)
🔮 Поддержка Go, Rust, TypeScript, C#

🔮 Асинхронные операции

🔮 AI-интеграция (NL to SQL)

🔮 Kubernetes-оптимизация

<div align="center">
AetherQuery Framework - универсальное решение для работы с базами данных в мультиязычных проектах

Документация • Примеры • Вопросы

</div>

AetherQuery = Ecosystem Language Programming + SQLite DB Layer + AI Model
📐 Четкая архитектура:
text
┌─────────────────────────────────────────────────┐
│            AetherQuery Ecosystem                │
├─────────────────────────────────────────────────┤
│  🌍 Ecosystem Language Programming              │
│     • Python (backend/ML)                       │
│     • TypeScript (frontend)                     │
│     • Rust (high-performance)                   │
│     • Единая спецификация моделей (YAML)        │
├─────────────────────────────────────────────────┤
│  💾 SQLite DB Layer                            │
│     • Универсальная файловая БД                 │
│     • Кросс-платформенность                    │
│     • Простота развертывания                   │
├─────────────────────────────────────────────────┤
│  🧠 AI Model (future)                          │
│     • Авто-генерация запросов                  │
│     • Интеллектуальная оптимизация             │
│     • NLP интерфейсы                           │
└─────────────────────────────────────────────────┤
🚀 Конкретный план на 4 недели:
Неделя 1: 🐍 Python Core + SQLite
python
# Фокус: Идеальный Python ORM
class AetherModel:
    # Базовый класс для всех моделей
    pass

class AetherQuery:
    # Мощный, но простой Query Builder
    def filter(self, **conditions): ...
    def all(self): ...
    def create(self, **data): ...

# Результат: 
✅ Production-ready Python ORM
✅ SQLite миграции  
✅ Документация и примеры
Неделя 2: 🌍 Language Ecosystem - TypeScript
typescript
// Фокус: TypeScript/JavaScript версия
class AetherQuery<T> {
    filter(conditions: Partial<T>): AetherQuery<T>
    all(): Promise<T[]>
    create(data: Partial<T>): Promise<T>
}

// Результат:
✅ Рабочий TypeScript ORM
✅ Совместимость API с Python
✅ Fullstack пример (Python backend + TS frontend)
Неделя 3: 🌍 Language Ecosystem - Rust
rust
// Фокус: High-performance Rust версия
#[derive(AetherModel)]
struct Task {
    id: i32,
    title: String,
    status: String,
}

impl AetherQuery for Task {
    fn filter(&self, conditions: &str) -> Self { ... }
    fn all(&self) -> Vec<Self> { ... }
}

// Результат:
✅ Базовый Rust ORM  
✅ Async/await поддержка
✅ Бенчмарки производительности
Неделя 4: 🎯 Integration + Specification
yaml
# Фокус: Единая спецификация
# models.yaml
User:
  table: users
  fields:
    name: 
      type: string
      required: true
      max_length: 100
    email:
      type: string  
      unique: true

# Результат:
✅ YAML → Code генератор
✅ Кросс-языковая совместимость
✅ Документация и релиз
💡 Почему это СУПЕР-сильная формула:
1. Ecosystem Language Programming
python
# Одна бизнес-логика - все языки
# Python (Data Science) + TypeScript (UI) + Rust (Performance)
2. SQLite DB Layer
python
# Универсальность + Простота
# Один файл .db работает везде:
# - Локальная разработка
# - Мобильные приложения
# - Встроенные системы
# - Прототипирование
3. AI Model (Future Ready)
python
# Архитектура готова для AI:
@ai_enhanced
class SmartQuery:
    def natural_language_query(self, text: str):
        # "Покажи задачи с высоким приоритетом за последнюю неделю"
        return self.filter(priority='high', created_at__gte='7d')
🎯 Конкретные измеримые цели:
К концу 4 недель:
bash
✅ Python: pip install aether-query
✅ TypeScript: npm install aether-query  
✅ Rust: cargo add aether_query
✅ Документация: aether-query.dev
✅ Примеры: 3 fullstack приложения
Пример рабочего кода:
python
# Одна модель - три языка
# Модель определяется ОДИН раз
# models/task.yaml
name: Task
fields:
  title: {type: string, required: true}
  status: {type: choice, choices: [todo, done]}

# Python
tasks = Task.query.filter(status='todo').all()

# TypeScript
const tasks = await Task.query().filter({status: 'todo'}).all()

# Rust  
let tasks = Task::query().filter("status", "todo").all().await?;
🔥 Уникальное торговое предложение:
Для разработчиков:
text
"Пиши бизнес-логику на любимом языке - 
данные будут одинаково работать везде"
Для бизнеса:
text
"Единая архитектура данных для:
- Web (Python/TypeScript) 
- Mobile (Rust)
- AI/ML (Python)
- High-load (Rust)
"
🚀 Начинаем с ПОНЕДЕЛЬНИКА:
День 1: Python AetherQuery стабилизация
python
# Чистим и доводим до идеала текущий код
# Фокус на:
- AetherQuery.filter() - мощный и предсказуемый
- AetherModel.save()/delete() - надежный
- SQLite миграции - простые но эффективные
День 2-3: Единая спецификация YAML
yaml
# Создаем формат описания моделей
# Который будет основой для всех языков
День 4-7: TypeScript кодогенерация
typescript
// Автоматическая генерация TS кода из YAML
// Базовые CRUD операции

Будущая структура проекта AetherQuery Ecosystem
text
aether-query/
├── 📁 spec/                 # Единая спецификация моделей
│   ├── models/             # YAML файлы моделей
│   ├── generators/         # Генераторы кода
│   └── validator.py        # Валидатор спецификаций
├── 📁 python/              # Python реализация
│   ├── aether_query/       # Python пакет
│   ├── models/            # Автосгенерированные модели
│   ├── tests/             # Тесты Python
│   └── pyproject.toml     # Конфиг Python пакета
├── 📁 typescript/          # TypeScript реализация  
│   ├── src/               # Исходный код TS
│   ├── generated/         # Автосгенерированные модели
│   ├── tests/             # Тесты TypeScript
│   └── package.json       # Конфиг npm пакета
├── 📁 rust/               # Rust реализация
│   ├── src/               # Исходный код Rust
│   ├── generated/         # Автосгенерированные модели
│   ├── tests/             # Тесты Rust
│   └── Cargo.toml         # Конфиг Rust пакета
├── 📁 examples/           # Примеры использования
│   ├── fullstack-app/     # Python backend + TS frontend
│   ├── mobile-app/        # Rust mobile пример
│   └── api-service/       # Микросервис пример
├── 📁 docs/               # Документация
│   ├── getting-started.md
│   ├── api-reference/
│   └── examples/
├── 📁 scripts/            # Вспомогательные скрипты
│   ├── generate.py        # Генератор кода
│   ├── build.py          # Сборка всех пакетов
│   └── test.py           # Запуск всех тестов
└── 📄 README.md           # Главная документация
🎯 Описание ключевых элементов:
spec/ - Единый источник правды
models/*.yaml - Описания моделей данных

generators/ - Шаблоны для кодогенерации

validator.py - Проверка корректности спецификаций

python/ - Реализация на Python
aether_query/ - Ядро ORM (AetherModel, AetherQuery)

models/ - Автосгенерированные Python классы

tests/ - Юнит-тесты и интеграционные тесты

typescript/ - Реализация на TypeScript
src/ - Ядро ORM на TypeScript

generated/ - Автосгенерированные TS интерфейсы

tests/ - Тесты для TypeScript версии

rust/ - Реализация на Rust
src/ - High-performance ORM на Rust

generated/ - Автосгенерированные Rust структуры

tests/ - Тесты и бенчмарки

examples/ - Рабочие примеры
fullstack-app/ - Демо полного стека

mobile-app/ - Пример для мобильных устройств

api-service/ - Микросервис архитектура

scripts/ - Автоматизация
generate.py - Генерация кода из YAML

build.py - Сборка всех пакетов

test.py - Запуск тестовой среды

Интегрированная структура проекта:
text
aether-query/                      # НОВЫЙ корень
├── 📁 legacy/                    # ⭐ СУЩЕСТВУЮЩИЙ ПРОЕКТ
│   └── AetherQuery_framework/    # Ваш текущий код
│       ├── src/aetherquery/      # ⭐ Ядро ORM
│       ├── examples/             # ⭐ Примеры БД
│       ├── tests/                # ⭐ Тесты адаптеров
│       └── pyproject.toml        # ⭐ Конфигурация
├── 📁 spec/                      # НОВОЕ: Спецификация
│   ├── models/                   # YAML модели
│   └── generators/               # Генераторы кода
├── 📁 python/                    # НОВОЕ: Чистый Python пакет
│   └── aetherquery/              # ⭐ Переносим ядро сюда
├── 📁 typescript/                # НОВОЕ: TS реализация
├── 📁 rust/                      # НОВОЕ: Rust реализация  
├── 📁 examples/                  # НОВОЕ: Примеры использования
│   ├── multi-db/                 # ⭐ Из legacy/examples/
│   ├── fullstack-app/            # Python backend + TS frontend
│   └── task-manager/             # Обновленный Task Manager
└── 📁 docs/                      # НОВОЕ: Документация
🎯 Ключевые элементы из вашего проекта:
⭐ Ценные активы:
src/aetherquery/ - Готовое ORM ядро ✅

examples/ - Рабочие примеры 5 БД ✅

tests/ - Тесты адаптеров ✅

pyproject.toml - Готовая конфигурация пакета ✅

План миграции (4 недели):
Неделя 1: Стабилизация + интеграция
python
# Сохраняем ВСЕ работающие функции:
✅ Мульти-БД адаптеры (SQLite, PostgreSQL, MySQL, MongoDB, Redis)
✅ Query Builder с цепочкой вызовов
✅ Конфигурация и исключения
✅ Существующие тесты
Неделя 2: Единая спецификация
yaml
# На основе работающего Python ORM создаем:
# spec/models/database.yaml - описание БД адаптеров
# spec/models/fields.yaml - типы полей
# spec/query/builder.yaml - синтаксис Query Builder
Неделя 3: TypeScript генерация
typescript
// Автогенерация TS кода из спецификации
// Сохраняя совместимость с Python API
export class AetherQuery {
  // Тот же API что и в Python
}
Неделя 4: Rust + документация
rust
// Rust версия с focus на производительность
// И полной совместимостью API
impl AetherQuery {
    // Тот же chainable API
}

Сильные стороны вашей текущей реализации:
Уже есть:
✅ Production-ready ORM ядро
✅ Поддержка 5 типов БД
✅ Тесты для всех адаптеров
✅ Рабочие примеры
✅ Пакетная конфигурация (pyproject.toml)

Наша задача:
🔄 Не сломать работающее
🚀 Расширить на другие языки
📐 Создать единую спецификацию
🌍 Построить экосистему
