"""Example usage of MySQL adapter"""

from python.aetherquery.db.connection import DatabaseConnection
from python.aetherquery.core.config import DatabaseConfig
import os


def check_mysql_availability():
    """Check if MySQL is available"""
    try:
        config = DatabaseConfig(
            type="mysql",
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            username=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            database=os.getenv('MYSQL_DB', 'test_db')
        )
        
        with DatabaseConnection(config) as db:
            return db.execute._adapter.test_connection()
    except Exception:
        return False


def mysql_example():
    """Demonstrate MySQL adapter usage"""
    
    if not check_mysql_availability():
        print("❌ MySQL is not available")
        print("💡 You can start MySQL with Docker:")
        print("   docker run -d --name mysql-test -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=test_db -p 3306:3306 mysql:8.0")
        return
    
    # Configuration for MySQL
    config = DatabaseConfig(
        type="mysql",
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        username=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'password'),
        database=os.getenv('MYSQL_DB', 'test_db')
    )
    
    try:
        # Using context manager for automatic connection management
        with DatabaseConnection(config) as db:
            print("✅ Connected to MySQL database")
            
            # Create table
            result = db.execute("""
                CREATE TABLE IF NOT EXISTS example_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
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
            
            # Show databases
            databases = db.execute._adapter.get_databases()
            print(f"\n🗃️ Available databases: {len(databases)}")
            
    except Exception as e:
        print(f"❌ MySQL operation failed: {e}")


if __name__ == "__main__":
    mysql_example()