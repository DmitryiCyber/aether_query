"""
AetherQuery Python Client

Минималистичный и эффективный клиент для работы с AetherQuery API.
"""

from .client import AetherClient
from .exceptions import (
    # Базовые исключения
    AetherQueryError,
    ConnectionError,
    TimeoutError,
    ConfigurationError,
    
    # Ошибки аутентификации и прав
    AuthenticationError,
    PermissionError,
    AuthError,  # Алиас
    
    # Ошибки валидации
    ValidationError,
    
    # Ошибки запросов
    QueryError,
    SyntaxError,
    ExecutionError,
    ResourceError,
    
    # Ошибки сервера
    ServerError,
    
    # Алиасы
    ConfigError,
)

__version__ = "0.1.0"
__author__ = "AetherQuery Team"
__email__ = "team@aetherquery.com"

__all__ = [
    # Клиент
    'AetherClient',
    
    # Исключения
    'AetherQueryError',
    'ConnectionError',
    'TimeoutError',
    'ConfigurationError',
    'AuthenticationError',
    'PermissionError',
    'AuthError',
    'ValidationError',
    'QueryError',
    'SyntaxError',
    'ExecutionError',
    'ResourceError',
    'ServerError',
    'ConfigError',
]

# Документация
__doc__ = """
AetherQuery Python Client

Простой и эффективный клиент для работы с AetherQuery API.
Поддерживает синхронные и асинхронные запросы, обработку ошибок,
валидацию и многое другое.

Пример использования:
    >>> from aetherquery import AetherClient
    >>> client = AetherClient("http://localhost:8000")
    >>> result = client.query("SELECT 1")
    >>> print(result)
"""