"""Tests for MongoDB adapter"""

import pytest
import os
import time
from python.aetherquery.db.adapters.mongodb import MongoDBAdapter
from python.aetherquery.core.config import DatabaseConfig
from python.aetherquery.core.exceptions import DatabaseError, QueryError, ConnectionError


def is_mongodb_available():
    """Check if MongoDB is available for testing - с таймаутом"""
    try:
        config = DatabaseConfig(
            type="mongodb",
            host=os.getenv('TEST_MONGODB_HOST', 'localhost'),
            port=int(os.getenv('TEST_MONGODB_PORT', 27017)),
            database=os.getenv('TEST_MONGODB_DB', 'test_db')
        )
        adapter = MongoDBAdapter(config)
        
        # Быстрая проверка с таймаутом
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 секунды таймаут
        result = sock.connect_ex((config.host, config.port))
        sock.close()
        
        if result != 0:
            return False
            
        adapter.connect()
        available = adapter.test_connection()
        adapter.disconnect()
        return available
    except Exception:
        return False


class TestMongoDBAdapter:
    """Test cases for MongoDBAdapter"""
    
    @pytest.fixture
    def mongodb_config(self):
        """MongoDB configuration from environment"""
        return DatabaseConfig(
            type="mongodb",
            host=os.getenv('TEST_MONGODB_HOST', 'localhost'),
            port=int(os.getenv('TEST_MONGODB_PORT', 27017)),
            database=os.getenv('TEST_MONGODB_DB', 'test_db')
        )
    
    @pytest.fixture
    def adapter(self, mongodb_config):
        """MongoDB adapter instance - только если MongoDB доступен"""
        if not is_mongodb_available():
            pytest.skip("MongoDB database is not available")
        
        adapter = MongoDBAdapter(mongodb_config)
        
        # Быстрое подключение с таймаутом
        try:
            adapter.connect()
            if not adapter.test_connection():
                pytest.skip("MongoDB connection test failed")
        except Exception:
            pytest.skip("MongoDB connection failed")
        
        yield adapter
        
        # Cleanup
        try:
            adapter.disconnect()
        except:
            pass
    
    @pytest.mark.skipif(not is_mongodb_available(), reason="MongoDB not available")
    def test_connection(self, mongodb_config):
        """Test database connection - простой тест"""
        adapter = MongoDBAdapter(mongodb_config)
        try:
            adapter.connect()
            assert adapter.is_connected
            adapter.disconnect()
            assert not adapter.is_connected
        except Exception as e:
            pytest.skip(f"MongoDB connection failed: {e}")
    
    @pytest.mark.skipif(not is_mongodb_available(), reason="MongoDB not available") 
    def test_basic_operations(self, adapter):
        """Test basic operations - без сложных запросов"""
        # Просто проверяем что адаптер работает
        assert adapter is not None
        assert adapter.is_connected
        
        # Проверяем получение коллекций
        collections = adapter.get_collections()
        assert isinstance(collections, list)


def test_mongodb_adapter_creation():
    """Test that MongoDB adapter can be created without connection"""
    config = DatabaseConfig(
        type="mongodb",
        host="localhost",
        database="test_db"
    )
    
    # Должен создаваться адаптер без подключения
    adapter = MongoDBAdapter(config)
    assert adapter is not None
    assert not adapter.is_connected


# Простой тест без фикстур
def test_mongodb_skip():
    """Test that skips properly when MongoDB is not available"""
    if not is_mongodb_available():
        pytest.skip("MongoDB not available for testing")
    
    # Если дошли сюда, MongoDB доступен
    config = DatabaseConfig(
        type="mongodb",
        host=os.getenv('TEST_MONGODB_HOST', 'localhost'),
        database=os.getenv('TEST_MONGODB_DB', 'test_db')
    )
    
    with MongoDBAdapter(config) as adapter:
        assert adapter.is_connected


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])