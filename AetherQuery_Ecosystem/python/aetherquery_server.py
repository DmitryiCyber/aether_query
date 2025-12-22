"""
Простой тестовый сервер AetherQuery для проверки подключения
Запуск: python aetherquery_server.py
"""

import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
import sys
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AetherQueryServer")

# Создаем приложение FastAPI
app = FastAPI(
    title="AetherQuery Test Server",
    description="Тестовый сервер для проверки подключения клиента",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    uptime: float

class QueryRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = 30

class QueryResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    execution_time: float
    query: str

class ServerInfo(BaseModel):
    name: str
    version: str
    description: str
    endpoints: List[str]
    started_at: str

# Состояние сервера
class ServerState:
    def __init__(self):
        self.start_time = datetime.now()
        self.query_count = 0
        self.is_healthy = True
    
    @property
    def uptime(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()

server_state = ServerState()

# Эндпоинты
@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "AetherQuery Test Server is running!",
        "docs": "/docs",
        "health": "/health",
        "info": "/info"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка здоровья сервера"""
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy" if server_state.is_healthy else "unhealthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=server_state.uptime
    )

@app.get("/info", response_model=ServerInfo)
async def server_info():
    """Информация о сервере"""
    endpoints = [
        "GET /",
        "GET /health",
        "GET /info",
        "POST /query",
        "GET /stats",
        "POST /execute",
        "GET /tables",
        "GET /table/{table_name}"
    ]
    
    return ServerInfo(
        name="AetherQuery Test Server",
        version="1.0.0",
        description="Тестовый сервер для проверки подключения AetherClient",
        endpoints=endpoints,
        started_at=server_state.start_time.isoformat()
    )

@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Выполнение SQL запроса"""
    import time
    start_time = time.time()
    server_state.query_count += 1
    
    logger.info(f"Executing query: {request.query}")
    
    # Имитация выполнения запроса
    await asyncio.sleep(0.1)
    
    # Примеры ответов для разных запросов
    query_lower = request.query.lower().strip()
    
    if "select" in query_lower and "users" in query_lower:
        data = [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "created_at": "2024-01-01"},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "created_at": "2024-01-02"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com", "created_at": "2024-01-03"}
        ]
        success = True
        error = None
    elif "select" in query_lower and "products" in query_lower:
        data = [
            {"id": 1, "name": "Product A", "price": 100, "stock": 50},
            {"id": 2, "name": "Product B", "price": 200, "stock": 30},
            {"id": 3, "name": "Product C", "price": 150, "stock": 20}
        ]
        success = True
        error = None
    elif "error" in query_lower:
        data = None
        success = False
        error = "Simulated query error: Syntax error near 'ERROR'"
    else:
        # Общий ответ
        data = [
            {"result": "success", "rows_affected": 1, "message": "Query executed successfully"}
        ]
        success = True
        error = None
    
    execution_time = time.time() - start_time
    
    return QueryResponse(
        success=success,
        data=data,
        error=error,
        execution_time=execution_time,
        query=request.query
    )

@app.get("/stats")
async def get_stats():
    """Статистика сервера"""
    return {
        "uptime": server_state.uptime,
        "query_count": server_state.query_count,
        "status": "running",
        "memory_usage": "simulated",
        "active_connections": 1
    }

@app.post("/execute")
async def execute_raw(request: Dict[str, Any]):
    """Выполнение сырого запроса"""
    logger.info(f"Raw execute: {request}")
    return {
        "success": True,
        "operation": request.get("operation", "unknown"),
        "result": "executed",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/tables")
async def list_tables():
    """Список таблиц"""
    return {
        "tables": [
            {"name": "users", "type": "table", "rows": 100},
            {"name": "products", "type": "table", "rows": 50},
            {"name": "orders", "type": "table", "rows": 200},
            {"name": "customers", "type": "table", "rows": 150}
        ]
    }

@app.get("/table/{table_name}")
async def table_info(table_name: str):
    """Информация о таблице"""
    return {
        "name": table_name,
        "columns": [
            {"name": "id", "type": "integer", "nullable": False},
            {"name": "name", "type": "varchar(255)", "nullable": True},
            {"name": "created_at", "type": "timestamp", "nullable": True}
        ],
        "estimated_rows": 100,
        "size_mb": 10.5
    }

# Простой HTTP сервер (альтернатива для тестирования)
class SimpleTestServer:
    """Простой HTTP сервер для базового тестирования"""
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        
    async def handle_request(self, reader, writer):
        """Обработчик запросов"""
        try:
            data = await reader.read(1024)
            request = data.decode()
            
            # Простой парсинг запроса
            if "GET /health" in request:
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    "\r\n"
                    '{"status": "healthy", "server": "AetherQuery"}'
                )
            elif "GET /" in request:
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "\r\n"
                    "AetherQuery Simple Test Server\n"
                    "Endpoints: /health, /info"
                )
            else:
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/plain\r\n"
                    "\r\n"
                    "Endpoint not found"
                )
            
            writer.write(response.encode())
            await writer.drain()
            
        except Exception as e:
            logger.error(f"Error handling request: {e}")
        finally:
            writer.close()
    
    async def run(self):
        """Запуск сервера"""
        server = await asyncio.start_server(
            self.handle_request,
            self.host,
            self.port
        )
        
        logger.info(f"Simple server started on {self.host}:{self.port}")
        
        async with server:
            await server.serve_forever()

def run_fastapi_server(host="0.0.0.0", port=8000, reload=False):
    """Запуск FastAPI сервера"""
    logger.info(f"🚀 Starting AetherQuery Test Server on {host}:{port}")
    logger.info(f"📚 Documentation: http://{host}:{port}/docs")
    logger.info(f"🔧 Health check: http://{host}:{port}/health")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

def run_simple_server(host="0.0.0.0", port=8000):
    """Запуск простого сервера"""
    logger.info(f"Starting simple test server on {host}:{port}")
    asyncio.run(SimpleTestServer(host, port).run())

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AetherQuery Test Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--simple", action="store_true", help="Use simple HTTP server instead of FastAPI")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (FastAPI only)")
    
    args = parser.parse_args()
    
    try:
        if args.simple:
            run_simple_server(args.host, args.port)
        else:
            run_fastapi_server(args.host, args.port, args.reload)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)