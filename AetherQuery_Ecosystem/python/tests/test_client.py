"""Минимальные тесты для AetherClient"""

import sys
import os

# Добавляем родительскую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from unittest.mock import Mock, patch
import pytest

try:
    from aetherquery.client import AetherClient
    from aetherquery.exceptions import (
        ConnectionError,
        TimeoutError,
        AuthenticationError,
        QueryError,
        ServerError,
    )
    IMPORT_SUCCESS = True
    print("✅ Импорт модулей успешен")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    IMPORT_SUCCESS = False


if IMPORT_SUCCESS:

    def test_client_initialization():
        """Тест инициализации клиента"""
        print("\n🧪 Тест: Инициализация клиента")
        client_instance = AetherClient(base_url="http://localhost:8000")
        assert client_instance.base_url == "http://localhost:8000"
        assert client_instance.timeout == 30.0
        assert client_instance.session is not None
        print("   ✅ Клиент инициализирован корректно")


    def test_client_with_api_key():
        """Тест клиента с API ключом"""
        print("\n🧪 Тест: Клиент с API ключом")
        client_instance = AetherClient(
            base_url="http://localhost:8000",
            api_key="test-key-12345"
        )
        assert client_instance.api_key == "test-key-12345"
        assert client_instance.session.headers['Authorization'] == "Bearer test-key-12345"
        print("   ✅ API ключ установлен корректно")


    @patch('aetherquery.client.requests.Session')
    def test_health_check(mock_session):
        """Тест проверки здоровья"""
        print("\n🧪 Тест: Проверка здоровья сервера")
        
        # Настраиваем мок
        mock_response = Mock()
        mock_response.json.return_value = {"status": "healthy", "version": "1.0.0"}
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_response
        
        # Создаем клиент и тестируем
        client_instance = AetherClient(base_url="http://localhost:8000")
        result = client_instance.health()
        
        assert result == {"status": "healthy", "version": "1.0.0"}
        print("   ✅ Health check отработал корректно")


    def test_client_context_manager():
        """Тест контекстного менеджера"""
        print("\n🧪 Тест: Контекстный менеджер (with statement)")
        with AetherClient(base_url="http://localhost:8000") as client_instance:
            assert isinstance(client_instance, AetherClient)
            assert client_instance.session is not None
            print("   ✅ Контекстный менеджер работает внутри блока")
        print("   ✅ Контекстный менеджер завершил работу")


    @patch('aetherquery.client.requests.Session')
    def test_connection_error(mock_session):
        """Тест ошибки соединения"""
        print("\n🧪 Тест: Ошибка соединения")
        
        import requests
        mock_session.return_value.request.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )
        
        client_instance = AetherClient(base_url="http://unreachable:9999")
        
        with pytest.raises(ConnectionError) as exc_info:
            client_instance.health()
        
        assert "Connection" in str(exc_info.value)
        print("   ✅ ConnectionError корректно обработан")


    @patch('aetherquery.client.requests.Session')
    def test_timeout_error(mock_session):
        """Тест таймаута"""
        print("\n🧪 Тест: Таймаут запроса")
        
        import requests
        mock_session.return_value.request.side_effect = requests.exceptions.Timeout(
            "Request timeout"
        )
        
        client_instance = AetherClient(base_url="http://localhost:8000", timeout=5.0)
        
        with pytest.raises(TimeoutError) as exc_info:
            client_instance.health()
        
        assert "5.0" in str(exc_info.value)
        print("   ✅ TimeoutError корректно обработан")


    def test_exceptions_hierarchy():
        """Тест иерархии исключений"""
        print("\n🧪 Тест: Иерархия исключений")
        
        # Проверяем наследование
        assert issubclass(ConnectionError, Exception)
        assert issubclass(TimeoutError, Exception)
        assert issubclass(AuthenticationError, Exception)
        assert issubclass(QueryError, Exception)
        assert issubclass(ServerError, Exception)
        
        print("   ✅ Иерархия исключений корректна")


    def run_all_tests():
        """Запуск всех тестов"""
        print("🚀 Запуск тестов AetherClient")
        print("=" * 50)
        
        tests = [
            test_client_initialization,
            test_client_with_api_key,
            test_health_check,
            test_client_context_manager,
            test_connection_error,
            test_timeout_error,
            test_exceptions_hierarchy,
        ]
        
        passed = 0
        failed = 0
        
        for test_func in tests:
            try:
                test_func()
                passed += 1
            except Exception as e:
                failed += 1
                print(f"   ❌ Тест {test_func.__name__} упал: {e}")
        
        print("\n" + "=" * 50)
        print(f"📊 Результаты:")
        print(f"   ✅ Успешно: {passed}")
        print(f"   ❌ Провалено: {failed}")
        print(f"   📈 Всего: {passed + failed}")
        
        if failed == 0:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        else:
            print(f"\n⚠️  {failed} тестов провалено")
        
        return failed == 0

else:
    
    def run_all_tests():
        print("❌ Тесты не могут быть запущены из-за ошибки импорта")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)