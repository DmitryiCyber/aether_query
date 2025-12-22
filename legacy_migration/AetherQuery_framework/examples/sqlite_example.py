"""Example usage of SQLite adapter"""

from python.aetherquery.db.connection import DatabaseConnection
from python.aetherquery.core.config import DatabaseConfig


def sqlite_example():
    """Demonstrate SQLite adapter usage"""
    
    # Configuration for in-memory database
    config = DatabaseConfig(type="sqlite", path=":memory:")
    
    # Using context manager for automatic connection management
    with DatabaseConnection(config) as db:
        print("✅ Connected to SQLite database")
        
        # Create table
        result = db.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print(f"✅ Table created: {result.success}")
        
        # Insert some data
        users = [
            {"username": "alice", "email": "alice@example.com"},
            {"username": "bob", "email": "bob@example.com"},
            {"username": "charlie", "email": "charlie@example.com"}
        ]
        
        for user in users:
            result = db.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                user
            )
            print(f"✅ Inserted user: {user['username']}, row count: {result.row_count}")
        
        # Query data
        result = db.execute("SELECT * FROM users ORDER BY username")
        print(f"\n✅ Query result: {result.row_count} users found")
        
        for row in result.rows:
            print(f"User: id={row[0]}, username={row[1]}, email={row[2]}, created={row[3]}")
        
        # Convert to dictionaries
        users_dict = result.to_dict()
        print(f"\n📋 As dictionaries:")
        for user in users_dict:
            print(f"  {user}")


if __name__ == "__main__":
    sqlite_example()