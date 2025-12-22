"""
Базовый пример использования AetherQuery клиента с обработкой исключений
"""

from aetherquery import AetherClient
from aetherquery.exceptions import (
    ConnectionError,
    TimeoutError,
    AuthenticationError,
    QueryError,
    ServerError,
)


def demonstrate_exceptions():
    """Демонстрация различных исключений"""
    print("🧪 Демонстрация исключений AetherQuery:")
    print("-" * 50)
    
    # 1. ConnectionError
    try:
        raise ConnectionError(
            message="Cannot connect to server",
            url="http://unreachable:9999",
            original_error=Exception("Network unreachable")
        )
    except ConnectionError as e:
        print(f"1. {e.__class__.__name__}: {e}")
        print(f"   URL: {e.url}")
        print(f"   Code: {e.code}")
    
    # 2. TimeoutError
    try:
        raise TimeoutError(timeout=30.0, operation="executing query")
    except TimeoutError as e:
        print(f"\n2. {e.__class__.__name__}: {e}")
        print(f"   Timeout: {e.timeout}s")
        print(f"   Operation: {e.operation}")
    
    # 3. AuthenticationError
    try:
        raise AuthenticationError(
            message="Invalid API key",
            reason="expired",
            status_code=401
        )
    except AuthenticationError as e:
        print(f"\n3. {e.__class__.__name__}: {e}")
        print(f"   Reason: {e.reason}")
        print(f"   Status: {e.status_code}")
    
    # 4. QueryError
    try:
        raise QueryError(
            message="Invalid SQL syntax",
            sql="SELEC * FROM users",  # Опечатка
            position=5
        )
    except QueryError as e:
        print(f"\n4. {e.__class__.__name__}: {e}")
        print(f"   SQL: {e.sql}")
        print(f"   Position: {e.position}")
    
    # 5. ServerError
    try:
        raise ServerError(
            message="Database connection pool exhausted",
            request_id="req_12345",
            status_code=503
        )
    except ServerError as e:
        print(f"\n5. {e.__class__.__name__}: {e}")
        print(f"   Request ID: {e.request_id}")
        print(f"   Status: {e.status_code}")


def main():
    print("🚀 Запуск базового примера AetherQuery клиента")
    print("=" * 60)
    
    # Демонстрация исключений
    demonstrate_exceptions()
    
    print("\n" + "=" * 60)
    print("🛠️  Пример использования клиента с обработкой ошибок:")
    print("-" * 60)
    
    # Создаем клиент
    client = AetherClient(
        base_url="http://localhost:8000",
        timeout=10.0
    )
    
    try:
        print("1. Клиент создан успешно")
        print(f"   • Base URL: {client.base_url}")
        print(f"   • Timeout: {client.timeout}s")
        print(f"   • Headers: {dict(client.session.headers)}")
        
        # Имитируем различные сценарии
        print("\n2. Возможные сценарии использования:")
        
        print("\n   Сценарий 1: Успешный запрос")
        print('   ```python')
        print('   try:')
        print('       result = client.query("SELECT 1")')
        print('       print(f"Result: {result}")')
        print('   except QueryError as e:')
        print('       print(f"Query failed: {e}")')
        print('   ```')
        
        print("\n   Сценарий 2: Обработка таймаута")
        print('   ```python')
        print('   try:')
        print('       result = client.query("SELECT sleep(10)")')
        print('   except TimeoutError as e:')
        print('       print(f"Timeout after {e.timeout}s")')
        print('   ```')
        
        print("\n   Сценарий 3: Обработка ошибок соединения")
        print('   ```python')
        print('   try:')
        print('       client.health()')
        print('   except ConnectionError as e:')
        print('       print(f"Cannot connect to {e.url}")')
        print('   ```')
        
        print("\n3. Использование контекстного менеджера:")
        print('   ```python')
        print('   with AetherClient("http://localhost:8000") as client:')
        print('       result = client.query("SELECT 1")')
        print('       # Автоматическое закрытие при выходе')
        print('   ```')
        
        print("\n🎉 Клиент готов к использованию!")
        print("\n📝 Для реального использования:")
        print("   1. Запустите сервер AetherQuery")
        print("   2. Настройте правильный base_url")
        print("   3. Добавьте API key если требуется")
        print("   4. Обрабатывайте исключения как показано выше")
        
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
    
    finally:
        client.close()
        print("\n🔒 Клиент закрыт")


if __name__ == "__main__":
    main()
