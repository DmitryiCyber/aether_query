"""Debug SQLite adapter to see what's happening"""

from python.aetherquery.db.adapters.sqlite import SQLiteAdapter
from python.aetherquery.core.config import DatabaseConfig


def debug_sqlite():
    """Debug SQLite operations"""
    
    config = DatabaseConfig(type="sqlite", path=":memory:")
    
    with SQLiteAdapter(config) as adapter:
        print("🔧 Testing CREATE TABLE...")
        
        # Test 1: Simple CREATE TABLE
        result1 = adapter.execute("CREATE TABLE test_simple (id INTEGER)")
        print(f"CREATE TABLE simple: success={result1.success}, row_count={result1.row_count}")
        
        # Test 2: CREATE TABLE with more columns
        result2 = adapter.execute("""
            CREATE TABLE test_products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL DEFAULT 0.0
            )
        """)
        print(f"CREATE TABLE products: success={result2.success}, row_count={result2.row_count}")
        
        # Test 3: INSERT
        result3 = adapter.execute(
            "INSERT INTO test_products (name, price) VALUES (?, ?)",
            {"name": "Test Product", "price": 99.99}
        )
        print(f"INSERT: success={result3.success}, row_count={result3.row_count}")
        
        # Test 4: SELECT
        result4 = adapter.execute("SELECT * FROM test_products")
        print(f"SELECT: success={result4.success}, row_count={result4.row_count}")
        print(f"SELECT columns: {result4.columns}")
        print(f"SELECT rows: {result4.rows}")
        
        # Test 5: Check tables
        tables = adapter.get_tables()
        print(f"Tables in database: {tables}")


if __name__ == "__main__":
    debug_sqlite()