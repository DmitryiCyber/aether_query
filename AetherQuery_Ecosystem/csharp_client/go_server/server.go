package main

import (
    "encoding/json"
    "net/http"
    "log"
    "strings"
)

func main() {
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{
            "status":  "healthy",
            "message": HealthCheck(),
            "version": "1.0",
        })
    })

    http.HandleFunc("/query", func(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    
    var query string
    
    // Определяем метод и формат запроса
    switch r.Method {
    case "GET":
        // GET с параметром ?q=
        query = r.URL.Query().Get("q")
        
    case "POST":
        contentType := r.Header.Get("Content-Type")
        
        if strings.Contains(contentType, "application/json") {
            // JSON POST: {"query": "SELECT ..."}
            var req struct { Query string `json:"query"` }
            if err := json.NewDecoder(r.Body).Decode(&req); err == nil {
                query = req.Query
            }
        } else {
            // Form POST: query=SELECT...
            query = r.FormValue("query")
        }
        
    default:
        http.Error(w, `{"error": "Method not allowed. Use GET with ?q= parameter or JSON POST"}`, http.StatusMethodNotAllowed)
        return
    }
    
    // Проверяем наличие запроса
    if query == "" {
        http.Error(w, `{"error": "Query parameter is required. Use ?q= for GET or {\"query\":\"...\"} for POST"}`, http.StatusBadRequest)
        return
    }
    
    // Обрабатываем запрос
    result := ProcessQuery(query)
    
    // Формируем ответ
    response := map[string]interface{}{
        "success": true,
        "query":   query,
        "result":  result,
        "method":  r.Method,
        "rows":    2, // пример
    }
    
    json.NewEncoder(w).Encode(response)
})

    log.Println("🚀 Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}