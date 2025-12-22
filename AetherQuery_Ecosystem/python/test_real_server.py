"""
Тестирование подключения к серверу AetherQuery
Теперь с поддержкой тестового сервера
"""

import sys
import os
import socket
import subprocess
import time
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def print_header(text):
    print("\n" + "="*60)
    print(f"📌 {text}")
    print("="*60)

def print_success(text):
    print(f"✅  {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_error(text):
    print(f"❌  {text}")

def print_info(text):
    print(f"ℹ️   {text}")

def check_server(host="localhost", port=8000, path="/health"):
    """Проверяет доступность сервера"""
    url = f"http://{host}:{port}{path}"
    
    try:
        # Сначала проверяем порт
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result != 0:
            return False, f"Port {port} is closed", None
        
        # Проверяем HTTP доступность
        req = Request(url, headers={'User-Agent': 'AetherQuery-Test'})
        response = urlopen(req, timeout=5)
        
        if response.status == 200:
            content = response.read().decode('utf-8')
            try:
                data = json.loads(content)
                return True, f"HTTP 200 - Server is healthy", data
            except:
                return True, f"HTTP 200 - {content[:100]}", content
        else:
            return False, f"HTTP {response.status}", None
            
    except socket.timeout:
        return False, "Connection timeout", None
    except ConnectionRefusedError:
        return False, "Connection refused", None
    except Exception as e:
        return False, str(e), None

def start_test_server():
    """Запускает тестовый сервер"""
    print_header("🚀 ЗАПУСК ТЕСТОВОГО СЕРВЕРА AETHERQUERY")
    
    # Проверяем зависимости
    try:
        import fastapi
        import uvicorn
        print_success("FastAPI и Uvicorn установлены")
    except ImportError:
        print_warning("FastAPI не установлен, устанавливаем...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"])
        print_success("Зависимости установлены")
    
    # Проверяем есть ли файл сервера
    server_file = "aetherquery_server.py"
    if not os.path.exists(server_file):
        print_error(f"Файл {server_file} не найден!")
        print("Создайте его с кодом сервера из инструкции")
        return False
    
    print_info(f"Найден файл сервера: {server_file}")
    
    # Запускаем сервер в фоновом режиме
    print_info("Запуск сервера на порту 8000...")
    
    try:
        # Проверяем не запущен ли уже сервер
        success, msg, _ = check_server("localhost", 8000)
        if success:
            print_success("Сервер уже запущен!")
            return True
        
        # Запускаем новый сервер
        import subprocess
        import threading
        
        def run_server():
            """Запускает сервер в отдельном процессе"""
            subprocess.run([sys.executable, server_file, "--port", "8000"])
        
        # Запускаем в отдельном потоке
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Ждем запуска
        print_info("Ожидание запуска сервера...")
        for i in range(10):
            time.sleep(1)
            success, msg, _ = check_server("localhost", 8000)
            if success:
                print_success(f"Сервер запущен! ({msg})")
                print_info(f"📚 Документация: http://localhost:8000/docs")
                print_info(f"🔧 Health check: http://localhost:8000/health")
                return True
            print(f"  Попытка {i+1}/10...")
        
        print_error("Не удалось запустить сервер")
        return False
        
    except Exception as e:
        print_error(f"Ошибка запуска сервера: {e}")
        return False

def test_connection():
    """Тестирует подключение к серверу"""
    print_header("🔗 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ")
    
    test_cases = [
        ("localhost", 8000, "/health"),
        ("127.0.0.1", 8000, "/health"),
        ("localhost", 8000, "/"),
        ("localhost", 8000, "/info"),
    ]
    
    all_success = True
    
    for host, port, path in test_cases:
        print(f"\n📡 Тестируем: http://{host}:{port}{path}")
        success, message, data = check_server(host, port, path)
        
        if success:
            print_success(f"  Успех: {message}")
            if data and isinstance(data, dict):
                if "status" in data:
                    print_success(f"  Статус: {data['status']}")
                if "version" in data:
                    print_success(f"  Версия: {data['version']}")
        else:
            print_error(f"  Ошибка: {message}")
            all_success = False
    
    return all_success

def test_with_curl():
    """Тестирует с помощью curl команд"""
    print_header("🔄 ТЕСТИРОВАНИЕ С CURL")
    
    commands = [
        ["curl", "-s", "http://localhost:8000/health"],
        ["curl", "-s", "http://localhost:8000/info"],
        ["curl", "-s", "http://localhost:8000/stats"],
    ]
    
    for cmd in commands:
        print(f"\n🔧 Выполняем: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print_success("  Успех!")
                try:
                    data = json.loads(result.stdout)
                    print(f"  Ответ: {json.dumps(data, ensure_ascii=False)[:100]}...")
                except:
                    print(f"  Ответ: {result.stdout[:100]}...")
            else:
                print_error(f"  Ошибка: {result.stderr}")
        except Exception as e:
            print_error(f"  Исключение: {e}")

def main():
    """Основная функция"""
    print_header("🔧 AETHERQUERY CONNECTION TESTER")
    print("Версия: 3.0 (с тестовым сервером)")
    
    # Вариант 1: Проверяем существующий сервер
    print("\n1. 🔍 ПРОВЕРКА СУЩЕСТВУЮЩЕГО СЕРВЕРА...")
    success = test_connection()
    
    if not success:
        print_header("⚠️  СЕРВЕР НЕ НАЙДЕН")
        
        # Спрашиваем пользователя
        response = input("\nЗапустить тестовый сервер AetherQuery? (y/n): ")
        
        if response.lower() in ['y', 'yes', 'да']:
            # Запускаем тестовый сервер
            if start_test_server():
                # Даем время на запуск
                time.sleep(2)
                
                # Тестируем подключение
                print_header("🧪 ТЕСТИРУЕМ ПОДКЛЮЧЕНИЕ К ТЕСТОВОМУ СЕРВЕРУ")
                test_connection()
                
                # Дополнительные тесты
                test_with_curl()
                
                print_header("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
                print("\nСервер работает! Теперь можете:")
                print("1. 📚 Открыть документацию: http://localhost:8000/docs")
                print("2. 🔧 Проверить здоровье: http://localhost:8000/health")
                print("3. 🚀 Протестировать клиент AetherQuery")
                
                # Предлагаем оставить сервер запущенным
                keep_running = input("\nОставить сервер запущенным? (y/n): ")
                if keep_running.lower() not in ['y', 'yes', 'да']:
                    print_info("Для остановки сервера нажмите Ctrl+C в окне сервера")
            else:
                print_error("Не удалось запустить тестовый сервер")
        else:
            print_info("Тестовый сервер не запущен")
            print("\nРучной запуск сервера:")
            print("  python aetherquery_server.py")
            print("Или с параметрами:")
            print("  python aetherquery_server.py --port 8000")
    else:
        print_header("✅ СЕРВЕР НАЙДЕН И РАБОТАЕТ")
        test_with_curl()
    
    print("\n" + "="*60)
    print("💡 ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:")
    print("="*60)
    print("Для запуска тестового сервера:")
    print("  python aetherquery_server.py")
    print("\nДля тестирования клиента:")
    print("  pip install aetherquery")
    print("  python -c \"from aetherquery import AetherClient; client = AetherClient('http://localhost:8000')\"")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Тестирование прервано")
        sys.exit(0)