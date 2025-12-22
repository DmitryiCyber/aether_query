"""Минимальный синхронный клиент для AetherQuery"""

import json
from typing import Optional, Dict, Any
import requests

from .exceptions import (
    AetherQueryError,
    ConnectionError,
    QueryError,
    AuthenticationError,
    TimeoutError,
)


class AetherClient:
    """Базовый синхронный клиент для работы с AetherQuery API"""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Инициализация клиента
        
        Args:
            base_url: Базовый URL API сервера
            api_key: Ключ API для аутентификации
            timeout: Таймаут запросов в секундах
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
        # Создаем сессию
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AetherQuery-Python-Client/0.1.0',
            'Accept': 'application/json',
        })
        
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Выполняет HTTP запрос с обработкой ошибок"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Добавляем таймаут
        kwargs.setdefault('timeout', self.timeout)
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timeout after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Connection failed")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 400:
                raise QueryError(f"Bad request: {e}")
            elif status_code == 401:
                raise AuthenticationError(f"Authentication failed: {e}")
            elif status_code == 403:
                raise AuthenticationError(f"Forbidden: {e}")
            else:
                raise AetherQueryError(f"HTTP error {status_code}: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request failed: {e}")
    
    def health(self) -> Dict[str, Any]:
        """Проверяет здоровье сервера"""
        return self._request('GET', '/health')
    
    def query(self, sql: str, params: Optional[list] = None) -> Dict[str, Any]:
        """
        Выполняет SQL запрос
        
        Args:
            sql: SQL запрос
            params: Параметры для prepared statements
            
        Returns:
            Результат выполнения запроса
        """
        payload = {'query': sql}
        if params:
            payload['params'] = params
            
        return self._request('POST', '/query', json=payload)
    
    def close(self):
        """Закрывает клиент и освобождает ресурсы"""
        self.session.close()
    
    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Поддержка контекстного менеджера"""
        self.close()