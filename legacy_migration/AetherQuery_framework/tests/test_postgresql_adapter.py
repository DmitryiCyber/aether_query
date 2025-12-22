"""Tests for PostgreSQL adapter"""

import pytest
import os
import time
from aetherquery.db.adapters.postgresql import PostgreSQLAdapter
from aetherquery.core.config import DatabaseConfig
from aetherquery.core.exceptions import DatabaseError, QueryError, ConnectionError


def is_postgresql_available():
    """Check if PostgreSQL is available for testing"""
    try:
        config = DatabaseConfig(
            type="postgresql",
            host=os.getenv('TEST_POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('TEST_POSTGRES_PORT', 5432)),
            username=os.getenv('TEST_POSTGRES_USER', 'postgres'),
            password=os.getenv('TEST_POSTGRES_PASSWORD', 'password'),
            database=os.getenv('TEST_POSTGRES_DB', 'test_db')
        )
        adapter = PostgreSQLAdapter(config)
        adapter.connect()
        available = adapter.test_connection()
        adapter.disconnect()
        return available
    except Exception:
        return False


class TestPostgreSQLAdapter:
    """Test cases for PostgreSQLAdapter"""
    
    @pytest.fixture
    def postgresql_config(self):
        """PostgreSQL configuration from environment"""
        return DatabaseConfig(
            type="postgresql",
            host=os.getenv('TEST_POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('TEST_POSTGRES_PORT', 5432)),
            username=os.getenv('TEST_POSTGRES_USER', 'postgres'),
            password=os.getenv('TEST_POSTGRES_PASSWORD', 'password'),
            database=os.getenv('TEST_POSTGRES_DB', 'test_db')
        )
    
    @pytest.fixture
    def adapter(self, postgresql_config):
        """PostgreSQL adapter instance"""
        if not is_postgresql_available():
            pytest.skip("PostgreSQL database is not available")
        
        adapter = PostgreSQLAdapter(postgresql_config)
        adapter.connect()
        
        # Создаем тестовую таблицу
        adapter.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Очищаем тестовые данные
        adapter.execute("DELETE FROM test_users")
        
        yield adapter
        
        # Cleanup
        adapter.execute("DROP TABLE IF EXISTS test_users")
        adapter.disconnect()
    
    @pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
    def test_connection(self, postgresql_config):
        """Test database connection"""
        adapter = PostgreSQLAdapter(postgresql_config)
        adapter.connect()
        assert adapter.is_connected
        adapter.disconnect()
        assert not adapter.is_connected
    
    @pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
    def test_create_table(self, adapter):
        """Test table creation"""
        result = adapter.execute("""
            CREATE TABLE test_products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                price DECIMAL(10,2) DEFAULT 0.0
            )
        """)
        assert result.success
        
        # Cleanup
        adapter.execute("DROP TABLE test_products")
    
    @pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
    def test_insert_data(self, adapter):
        """Test data insertion with named parameters"""
        result = adapter.execute(
            "INSERT INTO test_users (name, email) VALUES (%(name)s, %(email)s)",
            {"name": "John Doe", "email": "john@example.com"}
        )
        assert result.success
        assert result.row_count == 1
    
    @pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
    def test_select_data(self, adapter):
        """Test data selection"""
        # Setup test data
        adapter.execute(
            "INSERT INTO test_users (name, email) VALUES (%(name)s, %(email)s)",
            {"name": "Alice", "email": "alice@example.com"}
        )
        adapter.execute(
            "INSERT INTO test_users (name, email) VALUES (%(name)s, %(email)s)", 
            {"name": "Bob", "email": "bob@example.com"}
        )
        
        # Select data
        result = adapter.execute("SELECT * FROM test_users ORDER BY name")
        assert result.success
        assert result.row_count == 2
        assert 'id' in result.columns
        assert 'name' in result.columns
        assert 'email' in result.columns
    
    @pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
    def test_named_parameters(self, adapter):
        """Test named parameters support"""
        result = adapter.execute(
            "INSERT INTO test_users (name, email) VALUES (%(username)s, %(user_email)s)",
            {"username": "Test User", "user_email": "test@example.com"}
        )
        assert result.success
        assert result.row_count == 1
    
    @pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
    def test_get_tables(self, adapter):
        """Test getting table list"""
        tables = adapter.get_tables()
        assert 'test_users' in tables
    
    @pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
    def test_get_table_schema(self, adapter):
        """Test getting table schema"""
        schema = adapter.get_table_schema('test_users')
        assert len(schema) >= 3
        
        # Check column definitions
        column_names = [col['name'] for col in schema]
        assert 'id' in column_names
        assert 'name' in column_names
        assert 'email' in column_names


@pytest.mark.skipif(not is_postgresql_available(), reason="PostgreSQL not available")
def test_postgresql_extensions():
    """Test PostgreSQL extensions functionality"""
    config = DatabaseConfig(
        type="postgresql",
        host=os.getenv('TEST_POSTGRES_HOST', 'localhost'),
        username=os.getenv('TEST_POSTGRES_USER', 'postgres'),
        password=os.getenv('TEST_POSTGRES_PASSWORD', 'password'),
        database=os.getenv('TEST_POSTGRES_DB', 'test_db')
    )
    
    with PostgreSQLAdapter(config) as adapter:
        # Test extensions list
        extensions = adapter.get_extensions()
        assert isinstance(extensions, list)
        
        # Test creating extension (should fail if not exists, but that's OK)
        result = adapter.create_extension("nonexistent_extension")
        assert not result  # Should fail gracefully


def test_postgresql_adapter_creation():
    """Test that PostgreSQL adapter can be created without connection"""
    config = DatabaseConfig(
        type="postgresql",
        host="localhost",
        username="test",
        password="test", 
        database="test_db"
    )
    
    # Should be able to create adapter without connecting
    adapter = PostgreSQLAdapter(config)
    assert adapter is not None
    assert not adapter.is_connected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])