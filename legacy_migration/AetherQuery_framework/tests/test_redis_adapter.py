"""Tests for Redis adapter"""

import pytest
import os
import time
from aetherquery.db.adapters.redis import RedisAdapter
from aetherquery.core.config import DatabaseConfig
from aetherquery.core.exceptions import DatabaseError, QueryError, ConnectionError


def is_redis_available():
    """Check if Redis is available for testing"""
    try:
        config = DatabaseConfig(
            type="redis",
            host=os.getenv('TEST_REDIS_HOST', 'localhost'),
            port=int(os.getenv('TEST_REDIS_PORT', 6379)),
            username=os.getenv('TEST_REDIS_USER', ''),
            password=os.getenv('TEST_REDIS_PASSWORD', ''),
            database=os.getenv('TEST_REDIS_DB', '0')
        )
        adapter = RedisAdapter(config)
        
        # Быстрая проверка с таймаутом
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
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


class TestRedisAdapter:
    """Test cases for RedisAdapter"""
    
    @pytest.fixture
    def redis_config(self):
        """Redis configuration from environment"""
        return DatabaseConfig(
            type="redis",
            host=os.getenv('TEST_REDIS_HOST', 'localhost'),
            port=int(os.getenv('TEST_REDIS_PORT', 6379)),
            username=os.getenv('TEST_REDIS_USER', ''),
            password=os.getenv('TEST_REDIS_PASSWORD', ''),
            database=os.getenv('TEST_REDIS_DB', '0')
        )
    
    @pytest.fixture
    def adapter(self, redis_config):
        """Redis adapter instance"""
        if not is_redis_available():
            pytest.skip("Redis database is not available")
        
        adapter = RedisAdapter(redis_config)
        
        try:
            adapter.connect()
            if not adapter.test_connection():
                pytest.skip("Redis connection test failed")
        except Exception:
            pytest.skip("Redis connection failed")
        
        # Clean test database
        adapter.execute("FLUSHDB")
        
        yield adapter
        
        # Cleanup
        try:
            adapter.execute("FLUSHDB")
            adapter.disconnect()
        except:
            pass
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis not available")
    def test_connection(self, redis_config):
        """Test database connection"""
        adapter = RedisAdapter(redis_config)
        try:
            adapter.connect()
            assert adapter.is_connected
            adapter.disconnect()
            assert not adapter.is_connected
        except Exception as e:
            pytest.skip(f"Redis connection failed: {e}")
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis not available")
    def test_set_get(self, adapter):
        """Test SET and GET commands"""
        # Test SET
        result = adapter.execute("SET mykey myvalue")
        assert result.success
        
        # Test GET
        result = adapter.execute("GET mykey")
        assert result.success
        assert result.row_count == 1
        assert result.rows[0][0] == b'myvalue'
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis not available")
    def test_hash_operations(self, adapter):
        """Test hash operations"""
        # Test HSET
        result = adapter.execute("HSET user:1000 name John age 30")
        assert result.success
        
        # Test HGET
        result = adapter.execute("HGET user:1000 name")
        assert result.success
        assert result.rows[0][0] == b'John'
        
        # Test HGETALL
        result = adapter.execute("HGETALL user:1000")
        assert result.success
        assert result.row_count == 2
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis not available")
    def test_list_operations(self, adapter):
        """Test list operations"""
        # Test LPUSH
        result = adapter.execute("LPUSH mylist item1 item2 item3")
        assert result.success
        
        # Test LRANGE
        result = adapter.execute("LRANGE mylist 0 -1")
        assert result.success
        assert result.row_count == 3
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis not available")
    def test_keys_command(self, adapter):
        """Test KEYS command"""
        # Set some test keys
        adapter.execute("SET key1 value1")
        adapter.execute("SET key2 value2")
        
        result = adapter.execute("KEYS key*")
        assert result.success
        assert result.row_count >= 2
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis not available")
    def test_method_based_operations(self, adapter):
        """Test method-based operations"""
        # Test set/get methods
        success = adapter.set("method_key", "method_value")
        assert success
        
        value = adapter.get("method_key")
        assert value == b'method_value'
        
        # Test hash methods
        adapter.hset("user:2000", "name", "Alice")
        name = adapter.hget("user:2000", "name")
        assert name == b'Alice'
    
    @pytest.mark.skipif(not is_redis_available(), reason="Redis not available")
    def test_info_command(self, adapter):
        """Test INFO command"""
        result = adapter.execute("INFO")
        assert result.success
        assert result.row_count > 0
        
        # Test info method
        info = adapter.info()
        assert isinstance(info, dict)
        assert 'redis_version' in info


def test_redis_adapter_creation():
    """Test that Redis adapter can be created without connection"""
    config = DatabaseConfig(
        type="redis",  # Теперь это валидный тип
        host="localhost",
        database="0"
    )
    
    adapter = RedisAdapter(config)
    assert adapter is not None
    assert not adapter.is_connected


# Простой тест без фикстур
def test_redis_skip():
    """Test that skips properly when Redis is not available"""
    if not is_redis_available():
        pytest.skip("Redis not available for testing")
    
    config = DatabaseConfig(
        type="redis",
        host=os.getenv('TEST_REDIS_HOST', 'localhost'),
        database=os.getenv('TEST_REDIS_DB', '0')
    )
    
    with RedisAdapter(config) as adapter:
        assert adapter.is_connected


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])