"""
Исключения для AetherQuery Python клиента

Иерархия исключений:
- AetherQueryError (базовое)
  ├── ConnectionError (ошибки соединения)
  ├── TimeoutError (таймауты)
  ├── AuthenticationError (аутентификация)
  ├── PermissionError (права доступа)
  ├── ValidationError (валидация запросов)
  ├── QueryError (ошибки запросов)
  │   ├── SyntaxError (синтаксис SQL)
  │   ├── ExecutionError (выполнение запроса)
  │   └── ResourceError (ресурсы/лимиты)
  └── ServerError (ошибки сервера)
"""

from typing import Optional, Dict, Any, Union


class AetherQueryError(Exception):
    """
    Базовое исключение для всех ошибок AetherQuery API
    
    Attributes:
        message: Человекочитаемое описание ошибки
        code: Код ошибки API (если есть)
        details: Детальная информация об ошибке
        status_code: HTTP статус код (если есть)
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Union[str, Dict[str, Any]]] = None,
        status_code: Optional[int] = None
    ):
        self.message = message
        self.code = code
        self.details = details
        self.status_code = status_code
        
        # Формируем полное сообщение
        full_message = message
        if code:
            full_message = f"[{code}] {full_message}"
        if status_code:
            full_message = f"HTTP {status_code}: {full_message}"
            
        super().__init__(full_message)
    
    def __str__(self) -> str:
        return self.message
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует исключение в словарь"""
        result = {"message": self.message}
        if self.code:
            result["code"] = self.code
        if self.details:
            result["details"] = self.details
        if self.status_code:
            result["status_code"] = self.status_code
        return result


class ConnectionError(AetherQueryError):
    """Ошибка соединения с сервером AetherQuery"""
    
    def __init__(
        self,
        message: str = "Failed to connect to AetherQuery server",
        url: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        self.url = url
        self.original_error = original_error
        
        details = {}
        if url:
            details["url"] = url
        if original_error:
            details["original_error"] = str(original_error)
            
        super().__init__(
            message=message,
            code="CONNECTION_ERROR",
            details=details if details else None
        )


class TimeoutError(AetherQueryError):
    """Таймаут при выполнении запроса"""
    
    def __init__(
        self,
        timeout: float,
        operation: str = "request",
        url: Optional[str] = None
    ):
        self.timeout = timeout
        self.operation = operation
        self.url = url
        
        details = {
            "timeout_seconds": timeout,
            "operation": operation
        }
        if url:
            details["url"] = url
            
        super().__init__(
            message=f"Timeout after {timeout}s while {operation}",
            code="TIMEOUT_ERROR",
            details=details
        )


class AuthenticationError(AetherQueryError):
    """Ошибка аутентификации или авторизации"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        reason: Optional[str] = None,
        status_code: Optional[int] = 401
    ):
        self.reason = reason
        
        details = {}
        if reason:
            details["reason"] = reason
            
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            details=details if details else None,
            status_code=status_code
        )


class PermissionError(AetherQueryError):
    """Недостаточно прав для выполнения операции"""
    
    def __init__(
        self,
        message: str = "Insufficient permissions",
        required_permission: Optional[str] = None,
        status_code: Optional[int] = 403
    ):
        self.required_permission = required_permission
        
        details = {}
        if required_permission:
            details["required_permission"] = required_permission
            
        super().__init__(
            message=message,
            code="PERMISSION_ERROR",
            details=details if details else None,
            status_code=status_code
        )


class ValidationError(AetherQueryError):
    """Ошибка валидации входных данных"""
    
    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        value: Any = None,
        constraint: Optional[str] = None,
        status_code: Optional[int] = 422
    ):
        self.field = field
        self.value = value
        self.constraint = constraint
        
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        if constraint:
            details["constraint"] = constraint
            
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details=details if details else None,
            status_code=status_code
        )


class QueryError(AetherQueryError):
    """Базовое исключение для ошибок выполнения запросов"""
    
    def __init__(
        self,
        message: str,
        sql: Optional[str] = None,
        params: Optional[list] = None,
        position: Optional[int] = None,
        **kwargs
    ):
        self.sql = sql
        self.params = params
        self.position = position
        
        details = {}
        if sql:
            details["sql"] = sql
        if params:
            details["params"] = params
        if position is not None:
            details["position"] = position
            
        super().__init__(
            message=message,
            code="QUERY_ERROR",
            details=details if details else None,
            **kwargs
        )


class SyntaxError(QueryError):
    """Синтаксическая ошибка в SQL запросе"""
    
    def __init__(
        self,
        message: str = "SQL syntax error",
        sql: Optional[str] = None,
        position: Optional[int] = None
    ):
        super().__init__(
            message=message,
            sql=sql,
            position=position,
            code="SYNTAX_ERROR",
            status_code=400
        )


class ExecutionError(QueryError):
    """Ошибка выполнения SQL запроса"""
    
    def __init__(
        self,
        message: str = "Query execution failed",
        sql: Optional[str] = None,
        database_error: Optional[str] = None
    ):
        self.database_error = database_error
        
        details = {}
        if sql:
            details["sql"] = sql
        if database_error:
            details["database_error"] = database_error
            
        super().__init__(
            message=message,
            sql=sql,
            details=details if details else None,
            code="EXECUTION_ERROR",
            status_code=400
        )


class ResourceError(QueryError):
    """Ошибка из-за ограничений ресурсов"""
    
    def __init__(
        self,
        message: str = "Resource limit exceeded",
        resource_type: Optional[str] = None,
        limit: Optional[int] = None,
        used: Optional[int] = None
    ):
        self.resource_type = resource_type
        self.limit = limit
        self.used = used
        
        details = {}
        if resource_type:
            details["resource_type"] = resource_type
        if limit is not None:
            details["limit"] = limit
        if used is not None:
            details["used"] = used
            
        super().__init__(
            message=message,
            code="RESOURCE_ERROR",
            details=details if details else None,
            status_code=429  # Too Many Requests
        )


class ServerError(AetherQueryError):
    """Внутренняя ошибка сервера AetherQuery"""
    
    def __init__(
        self,
        message: str = "Internal server error",
        request_id: Optional[str] = None,
        status_code: Optional[int] = 500
    ):
        self.request_id = request_id
        
        details = {}
        if request_id:
            details["request_id"] = request_id
            
        super().__init__(
            message=message,
            code="SERVER_ERROR",
            details=details if details else None,
            status_code=status_code
        )


class ConfigurationError(AetherQueryError):
    """Ошибка конфигурации клиента"""
    
    def __init__(
        self,
        message: str = "Client configuration error",
        config_key: Optional[str] = None,
        config_value: Any = None
    ):
        self.config_key = config_key
        self.config_value = config_value
        
        details = {}
        if config_key:
            details["config_key"] = config_key
        if config_value is not None:
            details["config_value"] = config_value
            
        super().__init__(
            message=message,
            code="CONFIGURATION_ERROR",
            details=details if details else None
        )


# Короткие алиасы для удобства
AuthError = AuthenticationError
ConfigError = ConfigurationError