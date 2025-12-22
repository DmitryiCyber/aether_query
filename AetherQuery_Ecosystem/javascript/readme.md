# AetherQuery Goja Client

<div align="center">

![AetherQuery Logo](https://img.shields.io/badge/AetherQuery-Goja_Client-blue?style=for-the-badge)
![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?style=for-the-badge&logo=go)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Мощный JavaScript/TypeScript runtime для AetherQuery, построенный на Goja**

[Особенности](#особенности) • [Быстрый старт](#быстрый-старт) • [Использование](#использование) • [Документация API](#документация-api) • [Разработка](#разработка)

</div>

## 🚀 Особенности

### ✨ Основные возможности

- **🔄 Полная поддержка JavaScript ES6+** через движок Goja
- **📡 Интеграция с AetherQuery** для выполнения SQL запросов
- **🔧 Встроенные модули** для работы с базами данных и HTTP
- **💻 REPL окружение** для интерактивной разработки
- **📁 Выполнение скриптов** из файлов
- **🔌 Расширяемая архитектура** с системой модулей

### 🛠 Технический стек

- **Goja** - Pure Go JavaScript engine
- **Go 1.21+** - Язык реализации
- **ES6 Modules** - Система модулей
- **SQL-драйвер** - Интеграция с AetherQuery

## 🏁 Быстрый старт

### Предварительные требования

- Go 1.21 или новее
- AetherQuery сервер (опционально для тестирования)

### Установка

````bash
# Клонирование репозитория
git clone https://github.com/aetherquery/goja-client
cd goja-client

# Сборка проекта
go build -o aetherquery .

# Проверка установки
./aetherquery version

# Проверка версии
./aetherquery version

# Выполнение JavaScript кода
./aetherquery eval "2 + 2"

# Запуск REPL окружения
./aetherquery repl

# Выполнение скрипта
./aetherquery run examples/query.js

# Выполнение JavaScript файла
./aetherquery run script.js

# Интерактивный REPL
./aetherquery repl

# Выполнение кода напрямую
./aetherquery eval "aetherquery.health('http://localhost:8080')"

# Автоматическое определение (если аргумент - .js файл)
./aetherquery my-script.js

// example.js
const client = aetherquery.createClient('http://localhost:8080');

// Проверка здоровья сервера
const health = await client.health();
console.log('Server health:', health);

// Выполнение SQL запроса
const result = await client.query('SELECT * FROM users WHERE age > ?', [18]);
console.log('Users:', result.toObjects());

// Получение одного значения
const count = await client.fetchValue('SELECT COUNT(*) FROM users');
console.log('Total users:', count);

Интерактивный REPL
$ ./aetherquery repl
js> aetherquery.version
"1.0.0"
js> const result = await aetherquery.query('http://localhost:8080', 'SELECT 1 as test')
js> console.log(result.rows)
[[1]]
js> .exit

Документация API
Модуль aetherquery
aetherquery.createClient(baseURL, options)
Создает новый клиент для работы с AetherQuery сервером.

javascript
const client = aetherquery.createClient('http://localhost:8080', {
    timeout: 30000,
    retries: 3
});
aetherquery.query(baseURL, sql, params)
Выполняет SQL запрос и возвращает результат.

javascript
const result = await aetherquery.query(
    'http://localhost:8080',
    'SELECT * FROM users WHERE status = ?',
    ['active']
);
aetherquery.health(baseURL)
Проверяет доступность AetherQuery сервера.

javascript
const health = await aetherquery.health('http://localhost:8080');
// { status: 'healthy', timestamp: '...' }

Модуль utils
utils.formatDate(date)
Форматирует дату в ISO строку.

javascript
const now = utils.formatDate(); // "2024-01-15T10:30:00.000Z"
const custom = utils.formatDate(new Date('2023-12-01'));
utils.delay(ms)
Создает задержку на указанное количество миллисекунд.

javascript
await utils.delay(1000); // Ждет 1 секунду
Класс AetherQueryClient
client.query(sql, params)
javascript
const client = aetherquery.createClient('http://localhost:8080');
const result = await client.query('SELECT * FROM table', [param1, param2]);
client.fetchObjects(sql, params)
javascript
const users = await client.fetchObjects('SELECT * FROM users');
// Возвращает массив объектов: [{id: 1, name: 'John'}, ...]
client.fetchOne(sql, params)
javascript
const user = await client.fetchOne('SELECT * FROM users WHERE id = ?', [1]);
// Возвращает первый объект или null
client.fetchValue(sql, params)
javascript
const count = await client.fetchValue('SELECT COUNT(*) FROM users');
// Возвращает значение первой колонки первой строки

Архитектура
Структура проекта

goja-client/
├── internal/
│   ├── goja/           # Goja runtime обертка
│   │   ├── runtime.go  # Основной runtime
│   │   └── *.test.go   # Тесты
│   ├── core/           # Ядро клиента AetherQuery
│   └── js/             # JavaScript модули
├── main.go             # Точка входа CLI
└── examples/           # Примеры использования

Компоненты системы

CLI Интерфейс - Обработка командной строки
Goja Runtime - JavaScript движок и управление выполнением
Модульная система - Загрузка и управление JS модулями
AetherQuery Client - Go клиент для взаимодействия с сервером
REPL Окружение - Интерактивная среда выполнения

Разработка
Запуск тестов

bash
# Все тесты
go test -v ./...

# Тесты с покрытием
go test -v -race -cover ./...

# Конкретный пакет
go test -v ./internal/goja
Сборка и проверка
bash
# Сборка
go build -o aetherquery .

# Проверка качества кода
go vet ./...
gofmt -l .
Добавление новых модулей
Создайте JS файл в internal/js/api/

Добавьте модуль в функцию LoadModules() в runtime.go

Напишите тесты для нового функционала

🔧 Расширение
Добавление новых JavaScript модулей
go
// В runtime.go
modules := map[string]string{
    "mymodule": `
        mymodule = {
            hello: function() { return "Hello from new module!"; }
        };
    `,
}
Создание Go биндингов
go
func (r *Runtime) initGoBindings() error {
    // Регистрация Go функций в JavaScript
    r.vm.Set("goFunction", func(call goja.FunctionCall) goja.Value {
        // Логика функции
        return r.vm.ToValue("Hello from Go!")
    })
    return nil
}
📊 Производительность
Goja обеспечивает отличную производительность для JavaScript выполнения:

🚀 Быстрый запуск (нет JIT компиляции)

📉 Низкое потребление памяти

🔄 Эффективная интеграция Go/JavaScript

🤝 Вклад в проект
Мы приветствуем вклады в проект! Пожалуйста:

Форкните репозиторий

Создайте feature ветку (git checkout -b feature/amazing-feature)

Закоммитьте изменения (git commit -m 'Add amazing feature')

Запушьте в ветку (git push origin feature/amazing-feature)

Откройте Pull Request

Требования к коду
Соответствие Go code style

Покрытие тестами для нового функционала

Обновление документации

📄 Лицензия
Этот проект распространяется под MIT License - смотрите файл LICENSE для деталей.

🆘 Поддержка
📖 Документация AetherQuery

🐛 Отчеты об ошибках

💬 Обсуждения

🏷 Версии

<div align="center">
AetherQuery Goja Client - Мощный JavaScript runtime для ваших данных! 🚀

⬆ Наверх

</div> ```
Этот README.md предоставляет:

✅ Полное описание проекта и его возможностей

✅ Быстрый старт для новых пользователей

✅ Подробную документацию API

✅ Инструкции по разработке и расширению

✅ Профессиональное оформление с badges и структурированием

Теперь ваш проект имеет comprehensive документацию! 📚✨
````
