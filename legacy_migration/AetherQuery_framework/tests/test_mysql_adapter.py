"""Tests for MySQL adapter"""

import pytest
import os
from aetherquery.db.adapters.mysql import MySQLAdapter
from aetherquery.core.config import DatabaseConfig
from aetherquery.core.exceptions import DatabaseError, QueryError, ConnectionError


def is_mysql_available():
    """Check if MySQL is available for testing"""
    try:
        config = DatabaseConfig(
            type="mysql",
            host=os.getenv('TEST_MYSQL_HOST', 'localhost'),
            port=int(os.getenv('TEST_MYSQL_PORT', 3306)),
            username=os.getenv('TEST_MYSQL_USER', 'root'),
            password=os.getenv('TEST_MYSQL_PASSWORD', 'password'),
            database=os.getenv('TEST_MYSQL_DB', 'test_db')
        )
        adapter = MySQLAdapter(config)
        adapter.connect()
        available = adapter.test_connection()
        adapter.disconnect()
        return available
    except Exception:
        return False


class TestMySQLAdapter:
    """Test cases for MySQLAdapter"""
    
    @pytest.fixture
    def mysql_config(self):
        """MySQL configuration from environment"""
        return DatabaseConfig(
            type="mysql",
            host=os.getenv('TEST_MYSQL_HOST', 'localhost'),
            port=int(os.getenv('TEST_MYSQL_PORT', 3306)),
            username=os.getenv('TEST_MYSQL_USER', 'root'),
            password=os.getenv('TEST_MYSQL_PASSWORD', 'password'),
            database=os.getenv('TEST_MYSQL_DB', 'test_db')
        )
    
    @pytest.fixture
    def adapter(self, mysql_config):
        """MySQL adapter instance"""
        if not is_mysql_available():
            pytest.skip("MySQL database is not available")
        
        adapter = MySQLAdapter(mysql_config)
        adapter.connect()
        
        # Создаем тестовую таблицу
        adapter.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
    def test_connection(self, mysql_config):
        """Test database connection"""
        adapter = MySQLAdapter(mysql_config)
        adapter.connect()
        assert adapter.is_connected
        adapter.disconnect()
        assert not adapter.is_connected
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
    def test_create_table(self, adapter):
        """Test table creation"""
        result = adapter.execute("""
            CREATE TABLE test_products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                price DECIMAL(10,2) DEFAULT 0.0
            )
        """)
        assert result.success
        
        # Cleanup
        adapter.execute("DROP TABLE test_products")
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
    def test_insert_data(self, adapter):
        """Test data insertion with named parameters"""
        result = adapter.execute(
            "INSERT INTO test_users (name, email) VALUES (%(name)s, %(email)s)",
            {"name": "John Doe", "email": "john@example.com"}
        )
        assert result.success
        assert result.row_count == 1
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
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
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
    def test_named_parameters(self, adapter):
        """Test named parameters support"""
        result = adapter.execute(
            "INSERT INTO test_users (name, email) VALUES (%(username)s, %(user_email)s)",
            {"username": "Test User", "user_email": "test@example.com"}
        )
        assert result.success
        assert result.row_count == 1
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
    def test_get_tables(self, adapter):
        """Test getting table list"""
        tables = adapter.get_tables()
        assert 'test_users' in tables
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
    def test_get_table_schema(self, adapter):
        """Test getting table schema"""
        schema = adapter.get_table_schema('test_users')
        assert len(schema) >= 3
        
        # Check column definitions
        column_names = [col['name'] for col in schema]
        assert 'id' in column_names
        assert 'name' in column_names
        assert 'email' in column_names
    
    @pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
    def test_get_databases(self, adapter):
        """Test getting database list"""
        databases = adapter.get_databases()
        assert isinstance(databases, list)
        assert len(databases) > 0


@pytest.mark.skipif(not is_mysql_available(), reason="MySQL not available")
def test_mysql_transactions():
    """Test MySQL transactions"""
    config = DatabaseConfig(
        type="mysql",
        host=os.getenv('TEST_MYSQL_HOST', 'localhost'),
        username=os.getenv('TEST_MYSQL_USER', 'root'),
        password=os.getenv('TEST_MYSQL_PASSWORD', 'password'),
        database=os.getenv('TEST_MYSQL_DB', 'test_db')
    )
    
    with MySQLAdapter(config) as adapter:
        # Create test table
        adapter.execute("""
            CREATE TABLE IF NOT EXISTS test_transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                value VARCHAR(100)
            )
        """)
        
        # Test transaction
        adapter.begin_transaction()
        adapter.execute(
            "INSERT INTO test_transactions (value) VALUES (%(value)s)",
            {"value": "transaction_test"}
        )
        adapter.rollback()
        
        # Check that data was rolled back
        result = adapter.execute("SELECT COUNT(*) FROM test_transactions")
        assert result.rows[0][0] == 0
        
        # Cleanup
        adapter.execute("DROP TABLE test_transactions")


def test_mysql_adapter_creation():
    """Test that MySQL adapter can be created without connection"""
    config = DatabaseConfig(
        type="mysql",
        host="localhost",
        username="test",
        password="test", 
        database="test_db"
    )
    
    # Should be able to create adapter without connecting
    adapter = MySQLAdapter(config)
    assert adapter is not None
    assert not adapter.is_connected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])