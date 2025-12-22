"""Example usage of PostgreSQL adapter"""

from python.aetherquery.db.connection import DatabaseConnection
from python.aetherquery.core.config import DatabaseConfig
import os


def check_postgresql_availability():
    """Check if PostgreSQL is available"""
    try:
        config = DatabaseConfig(
            type="postgresql",
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', 5432)),
            username=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'password'),
            database=os.getenv('POSTGRES_DB', 'test_db')
        )
        
        with DatabaseConnection(config) as db:
            return db.execute._adapter.test_connection()
    except Exception:
        return False


def postgresql_example():
    """Demonstrate PostgreSQL adapter usage"""
    
    if not check_postgresql_availability():
        print("❌ PostgreSQL is not available")
        print("💡 You can start PostgreSQL with Docker:")
        print("   docker run -d --name postgres-test -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test_db -p 5432:5432 postgres:15")
        return
    
    # Configuration for PostgreSQL
    config = DatabaseConfig(
        type="postgresql",
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        username=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        database=os.getenv('POSTGRES_DB', 'test_db')
    )
    
    try:
        # Using context manager for automatic connection management
        with DatabaseConnection(config) as db:
            print("✅ Connected to PostgreSQL database")
            
            # Create table
            result = db.execute("""
                CREATE TABLE IF NOT EXISTS example_users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print(f"✅ Table created/verified: {result.success}")
            
            # Insert some data with named parameters
            users = [
                {"username": "alice", "email": "alice@example.com"},
                {"username": "bob", "email": "bob@example.com"},
                {"username": "charlie", "email": "charlie@example.com"}
            ]
            
            for user in users:
                result = db.execute(
                    "INSERT INTO example_users (username, email) VALUES (%(username)s, %(email)s)",
                    user
                )
                print(f"✅ Inserted user: {user['username']}, row count: {result.row_count}")
            
            # Query data
            result = db.execute("SELECT * FROM example_users ORDER BY username")
            print(f"\n✅ Query result: {result.row_count} users found")
            
            for row in result.rows:
                print(f"User: id={row[0]}, username={row[1]}, email={row[2]}, created={row[3]}")
            
    except Exception as e:
        print(f"❌ PostgreSQL operation failed: {e}")


if __name__ == "__main__":
    postgresql_example()