"""Tests for SQLite adapter"""

import pytest
import tempfile
import os
import time
from aetherquery.db.adapters.sqlite import SQLiteAdapter
from aetherquery.core.config import DatabaseConfig
from aetherquery.core.exceptions import DatabaseError, QueryError


class TestSQLiteAdapter:
    """Test cases for SQLiteAdapter"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database file"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        yield db_path
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @pytest.fixture
    def sqlite_config(self, temp_db):
        """SQLite configuration"""
        return DatabaseConfig(
            type="sqlite",
            path=temp_db
        )
    
    @pytest.fixture
    def adapter(self, sqlite_config):
        """SQLite adapter instance"""
        adapter = SQLiteAdapter(sqlite_config)
        adapter.connect()
        yield adapter
        adapter.disconnect()
    
    def test_connection(self, sqlite_config):
        """Test database connection"""
        adapter = SQLiteAdapter(sqlite_config)
        adapter.connect()
        assert adapter.is_connected
        adapter.disconnect()
        assert not adapter.is_connected
    
    def test_in_memory_db(self):
        """Test in-memory database"""
        config = DatabaseConfig(type="sqlite", path=":memory:")
        adapter = SQLiteAdapter(config)
        adapter.connect()
        assert adapter.is_connected
        
        # Простой тест создания таблицы в памяти
        result = adapter.execute("CREATE TABLE memory_test (id INTEGER)")
        assert result.success
        adapter.disconnect()
    
    def test_create_table(self, adapter):
        """Test table creation"""
        result = adapter.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL DEFAULT 0.0
            )
        """)
        assert result.success
        # DDL операции (CREATE TABLE) могут возвращать rowcount = 0 или -1
        # Главное что операция успешна
        assert result.row_count >= 0
    
    def test_insert_data(self, adapter):
        """Test data insertion"""
        # Сначала создаем таблицу
        adapter.execute("""
            CREATE TABLE test_insert (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value TEXT
            )
        """)
        
        # Insert data using positional parameters
        result = adapter.execute(
            "INSERT INTO test_insert (name, value) VALUES (?, ?)",
            {"name": "John Doe", "value": "test_value"}
        )
        assert result.success
        assert result.row_count == 1
    
    def test_select_data(self, adapter):
        """Test data selection"""
        # Setup test data
        adapter.execute("""
            CREATE TABLE test_select (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        """)
        
        adapter.execute(
            "INSERT INTO test_select (name, email) VALUES (?, ?)",
            {"name": "Alice", "email": "alice@example.com"}
        )
        adapter.execute(
            "INSERT INTO test_select (name, email) VALUES (?, ?)", 
            {"name": "Bob", "email": "bob@example.com"}
        )
        
        # Select data
        result = adapter.execute("SELECT * FROM test_select ORDER BY name")
        assert result.success
        assert result.row_count == 2
        assert result.columns == ['id', 'name', 'email']
        assert len(result.rows) == 2
        
        # Проверяем данные (id автоинкремент, поэтому начинаем с name)
        assert result.rows[0][1] == 'Alice'  # name
        assert result.rows[0][2] == 'alice@example.com'  # email
        assert result.rows[1][1] == 'Bob'
        assert result.rows[1][2] == 'bob@example.com'
    
    def test_invalid_query(self, adapter):
        """Test handling of invalid queries"""
        result = adapter.execute("INVALID SQL QUERY")
        assert not result.success
    
    def test_get_tables(self, adapter):
        """Test getting table list"""
        adapter.execute("CREATE TABLE table1 (id INTEGER)")
        adapter.execute("CREATE TABLE table2 (id INTEGER)")
        
        tables = adapter.get_tables()
        assert 'table1' in tables
        assert 'table2' in tables
    
    def test_get_table_schema(self, adapter):
        """Test getting table schema"""
        adapter.execute("""
            CREATE TABLE test_schema (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                value REAL DEFAULT 0.0
            )
        """)
        
        schema = adapter.get_table_schema('test_schema')
        assert len(schema) == 3
        
        # Check column definitions
        column_names = [col['name'] for col in schema]
        assert 'id' in column_names
        assert 'name' in column_names
        assert 'value' in column_names


def test_simple_workflow():
    """Simple integration test"""
    config = DatabaseConfig(type="sqlite", path=":memory:")
    
    with SQLiteAdapter(config) as adapter:
        # Create table
        result = adapter.execute("""
            CREATE TABLE books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT
            )
        """)
        assert result.success
        
        # Insert data
        result = adapter.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
        )
        assert result.success
        assert result.row_count == 1
        
        # Query data
        result = adapter.execute("SELECT * FROM books")
        assert result.success
        assert result.row_count == 1
        assert result.rows[0][1] == "The Great Gatsby"


def test_ddl_operations():
    """Test that DDL operations work correctly"""
    config = DatabaseConfig(type="sqlite", path=":memory:")
    
    with SQLiteAdapter(config) as adapter:
        # Test CREATE TABLE
        result = adapter.execute("CREATE TABLE test1 (id INTEGER)")
        assert result.success
        assert result.row_count >= 0  # Может быть 0 или -1 для DDL
        
        # Test DROP TABLE
        result = adapter.execute("DROP TABLE test1")
        assert result.success
        assert result.row_count >= 0
        
        # Test multiple DDL operations
        result = adapter.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        assert result.success
        
        result = adapter.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount REAL
            )
        """)
        assert result.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])