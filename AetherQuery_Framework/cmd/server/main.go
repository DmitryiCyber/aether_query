// cmd/server/main.go
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

func main() {
	port := ":8080"
	if p := os.Getenv("PORT"); p != "" {
		port = ":" + p
	}

	fmt.Println("✨ Aether Query Server")
	fmt.Println("📡 Адрес: http://localhost" + port)
	fmt.Println("🕐 Время запуска:", time.Now().Format("15:04:05"))
	fmt.Println()

	// Настройка маршрутов
	http.HandleFunc("/", handleRoot)
	http.HandleFunc("/health", handleHealth)
	http.HandleFunc("/query", handleQuery)
	http.HandleFunc("/query/examples", handleQueryExamples)
	http.HandleFunc("/clients", handleClients)
	http.HandleFunc("/server/info", handleServerInfo)

	// Запуск сервера
	log.Printf("🚀 Сервер запущен на порту %s", port)
	log.Printf("📊 Доступные эндпоинты:")
	log.Printf("  GET  /                 - Информация о сервере")
	log.Printf("  GET  /health           - Проверка здоровья")
	log.Printf("  POST /query            - Выполнение запроса")
	log.Printf("  GET  /query/examples   - Примеры запросов")
	log.Printf("  GET  /clients          - Список клиентов")
	log.Printf("  GET  /server/info      - Информация о сервере")
	
	if err := http.ListenAndServe(port, nil); err != nil {
		log.Fatal("❌ Ошибка запуска сервера:", err)
	}
}

// Структуры данных
type ServerInfo struct {
	Name        string    `json:"name"`
	Version     string    `json:"version"`
	Description string    `json:"description"`
	StartTime   time.Time `json:"start_time"`
	Uptime      string    `json:"uptime"`
}

type HealthStatus struct {
	Status    string `json:"status"`
	Timestamp string `json:"timestamp"`
	Message   string `json:"message"`
}

type QueryRequest struct {
	Query  string                 `json:"query"`
	Parameters map[string]interface{} `json:"parameters"`
}

type QueryResponse struct {
	Success  bool                   `json:"success"`
	Query    string                 `json:"query,omitempty"`
	Data     interface{}            `json:"data,omitempty"`
	Error    string                 `json:"error,omitempty"`
	Duration string                 `json:"duration"`
	Rows     int                    `json:"rows,omitempty"`
	Columns  []string               `json:"columns,omitempty"`
}

type ClientInfo struct {
	Name        string   `json:"name"`
	Language    string   `json:"language"`
	Status      string   `json:"status"`
	Version     string   `json:"version"`
	Description string   `json:"description"`
	Features    []string `json:"features"`
}

// Глобальные переменные
var serverStartTime = time.Now()
var supportedClients = []ClientInfo{
	{
		Name:        "Python Client",
		Language:    "Python",
		Status:      "✅ Готов",
		Version:     "1.0.0",
		Description: "Асинхронный клиент для Python 3.8+",
		Features:    []string{"SQL запросы", "Асинхронность", "Типизация"},
	},
	{
		Name:        "JavaScript Client",
		Language:    "JavaScript/TypeScript",
		Status:      "🔄 В разработке",
		Version:     "0.9.0",
		Description: "Клиент для Node.js и браузеров",
		Features:    []string{"Promise-based", "TypeScript типы", "React hooks"},
	},
	{
		Name:        "Go Client",
		Language:    "Go",
		Status:      "✅ Готов",
		Version:     "1.0.0",
		Description: "Нативный Go клиент (этот сервер)",
		Features:    []string{"Высокая производительность", "Горутины", "Мультиплатформенность"},
	},
	{
		Name:        "Rust Client",
		Language:    "Rust",
		Status:      "🔄 В разработке",
		Version:     "0.5.0",
		Description: "Безопасный и быстрый клиент на Rust",
		Features:    []string{"Безопасность памяти", "Асинхронность", "WASM поддержка"},
	},
	{
		Name:        "C# Client",
		Language:    "C#/.NET",
		Status:      "✅ Готов",
		Version:     "1.0.0",
		Description: "Клиент для .NET и Avalonia UI",
		Features:    []string{"Avalonia UI", "async/await", "Кроссплатформенность"},
	},
}

// Обработчики
func handleRoot(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	info := map[string]interface{}{
		"name":        "Aether Query Server",
		"version":     "1.0.0",
		"description": "Минималистичный SQL-сервер для Aether Studio",
		"author":      "AetherQuery Team",
		"license":     "MIT",
		"repository":  "github.com/aetherquery/framework",
		"timestamp":   time.Now().Format(time.RFC3339),
		"endpoints": []map[string]string{
			{"method": "GET", "path": "/", "description": "Информация о сервере"},
			{"method": "GET", "path": "/health", "description": "Проверка здоровья"},
			{"method": "POST", "path": "/query", "description": "Выполнение запроса"},
			{"method": "GET", "path": "/query/examples", "description": "Примеры запросов"},
			{"method": "GET", "path": "/clients", "description": "Список клиентов"},
			{"method": "GET", "path": "/server/info", "description": "Информация о сервере"},
		},
	}

	sendJSON(w, info)
}

func handleHealth(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	status := HealthStatus{
		Status:    "healthy",
		Timestamp: time.Now().Format("2006-01-02 15:04:05"),
		Message:   "Сервер работает нормально",
	}

	sendJSON(w, status)
}

func handleQuery(w http.ResponseWriter, r *http.Request) {
	startTime := time.Now()

	// Поддержка CORS
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}

	if r.Method == "GET" {
		// GET запрос с параметром q
		query := r.URL.Query().Get("q")
		if query == "" {
			query = "SELECT * FROM users LIMIT 5"
		}

		response := executeQuery(query, nil, startTime)
		sendJSON(w, response)
		return
	}

	if r.Method == "POST" {
		// POST запрос с JSON телом
		var req QueryRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			response := QueryResponse{
				Success:  false,
				Error:    "Invalid JSON: " + err.Error(),
				Duration: time.Since(startTime).String(),
			}
			sendJSON(w, response)
			return
		}

		response := executeQuery(req.Query, req.Parameters, startTime)
		sendJSON(w, response)
		return
	}

	http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
}

func handleQueryExamples(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	examples := map[string]interface{}{
		"sql": map[string][]string{
			"basic": {
				"SELECT * FROM users",
				"SELECT name, email FROM users WHERE active = true",
				"SELECT COUNT(*) as total FROM users",
				"SELECT * FROM products ORDER BY price DESC LIMIT 10",
			},
			"advanced": {
				"INSERT INTO users (name, email) VALUES ('John', 'john@example.com')",
				"UPDATE users SET active = false WHERE last_login < '2024-01-01'",
				"DELETE FROM logs WHERE created_at < DATE('now', '-30 days')",
				"CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)",
			},
		},
		"python": []string{
			"import aether\nresult = aether.query('SELECT * FROM users LIMIT 5')\nfor row in result:\n    print(f\"{row['name']}: {row['email']}\")",
			"async with aether.AsyncClient() as client:\n    data = await client.execute('SELECT * FROM products WHERE price > 100')\n    print(f'Найдено {len(data)} товаров')",
		},
		"javascript": []string{
			"const result = await aether.query('SELECT * FROM users WHERE active = ?', [true]);\nconsole.log(`Активных пользователей: ${result.length}`);",
			"// Использование с React\nconst { data, loading } = useAetherQuery('SELECT * FROM products');",
		},
		"rust": []string{
			"let client = AetherClient::new(\"http://localhost:8080\");\nlet result = client.execute_query(\"SELECT * FROM users\").await?;\nprintln!(\"{:?}\", result);",
		},
		"go": []string{
			"client := aether.NewClient(\"http://localhost:8080\")\nresult, err := client.Query(ctx, \"SELECT * FROM users\")\nif err != nil {\n    log.Fatal(err)\n}\nfmt.Printf(\"Результат: %+v\\n\", result)",
		},
	}

	sendJSON(w, examples)
}

func handleClients(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	sendJSON(w, map[string]interface{}{
		"clients": supportedClients,
		"count":   len(supportedClients),
		"timestamp": time.Now().Format(time.RFC3339),
	})
}

func handleServerInfo(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	info := ServerInfo{
		Name:        "Aether Query Server",
		Version:     "1.0.0",
		Description: "Минималистичный автономный SQL-сервер",
		StartTime:   serverStartTime,
		Uptime:      time.Since(serverStartTime).String(),
	}

	sendJSON(w, info)
}

// Вспомогательные функции
func executeQuery(query string, params map[string]interface{}, startTime time.Time) QueryResponse {
	// Имитация выполнения запроса
	time.Sleep(time.Millisecond * 50)

	// Генерация тестовых данных на основе запроса
	queryType := "SELECT"
	if len(query) > 6 {
		cmd := query[:6]
		switch cmd {
		case "INSERT":
			queryType = "INSERT"
		case "UPDATE":
			queryType = "UPDATE"
		case "DELETE":
			queryType = "DELETE"
		case "CREATE":
			queryType = "CREATE"
		}
	}

	switch queryType {
	case "SELECT":
		// Генерация тестовых данных
		data := generateMockData(query)
		return QueryResponse{
			Success:  true,
			Query:    query,
			Data:     data,
			Duration: time.Since(startTime).String(),
			Rows:     len(data),
			Columns:  []string{"id", "name", "email", "status", "created_at"},
		}

	case "INSERT", "UPDATE", "DELETE", "CREATE":
		return QueryResponse{
			Success:  true,
			Query:    query,
			Data:     map[string]interface{}{"affected_rows": 1, "last_insert_id": 42},
			Duration: time.Since(startTime).String(),
			Rows:     1,
		}

	default:
		return QueryResponse{
			Success:  false,
			Query:    query,
			Error:    "Unsupported query type",
			Duration: time.Since(startTime).String(),
		}
	}
}

func generateMockData(query string) []map[string]interface{} {
	// База тестовых данных
	users := []map[string]interface{}{
		{"id": 1, "name": "Алексей Петров", "email": "alexey@example.com", "status": "active", "created_at": "2024-01-15"},
		{"id": 2, "name": "Мария Иванова", "email": "maria@example.com", "status": "active", "created_at": "2024-02-20"},
		{"id": 3, "name": "Иван Сидоров", "email": "ivan@example.com", "status": "inactive", "created_at": "2024-03-10"},
		{"id": 4, "name": "Ольга Козлова", "email": "olga@example.com", "status": "active", "created_at": "2024-04-05"},
		{"id": 5, "name": "Дмитрий Фёдоров", "email": "dmitry@example.com", "status": "pending", "created_at": "2024-05-12"},
		{"id": 6, "name": "Екатерина Морозова", "email": "ekaterina@example.com", "status": "active", "created_at": "2024-06-18"},
		{"id": 7, "name": "Сергей Николаев", "email": "sergey@example.com", "status": "inactive", "created_at": "2024-07-22"},
		{"id": 8, "name": "Анна Павлова", "email": "anna@example.com", "status": "active", "created_at": "2024-08-30"},
		{"id": 9, "name": "Павел Волков", "email": "pavel@example.com", "status": "active", "created_at": "2024-09-14"},
		{"id": 10, "name": "Наталья Семёнова", "email": "natalia@example.com", "status": "pending", "created_at": "2024-10-25"},
	}

	// Простая фильтрация на основе запроса
	var result []map[string]interface{}
	
	// Проверяем наличие LIMIT
	limit := 10
	if contains(query, "LIMIT") {
		// Простая логика для демо
		limit = 5
	}

	// Проверяем фильтры
	for i, user := range users {
		if i >= limit {
			break
		}

		include := true
		
		// Фильтр по статусу
		if contains(query, "WHERE status = 'active'") {
			if user["status"] != "active" {
				include = false
			}
		} else if contains(query, "WHERE status = 'inactive'") {
			if user["status"] != "inactive" {
				include = false
			}
		}

		if include {
			result = append(result, user)
		}
	}

	return result
}

func contains(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

func sendJSON(w http.ResponseWriter, data interface{}) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	json.NewEncoder(w).Encode(data)
}