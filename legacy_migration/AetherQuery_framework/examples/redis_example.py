"""Example usage of Redis adapter"""

from python.aetherquery.db.connection import DatabaseConnection
from python.aetherquery.core.config import DatabaseConfig
import os


def check_redis_availability():
    """Check if Redis is available"""
    try:
        config = DatabaseConfig(
            type="redis",
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            database=os.getenv('REDIS_DB', '0')
        )
        
        with DatabaseConnection(config) as db:
            return db.execute._adapter.test_connection()
    except Exception:
        return False


def redis_example():
    """Demonstrate Redis adapter usage"""
    
    if not check_redis_availability():
        print("❌ Redis is not available")
        print("💡 You can start Redis with Docker:")
        print("   docker run -d --name redis-test -p 6379:6379 redis:7.0")
        return
    
    # Configuration for Redis
    config = DatabaseConfig(
        type="redis",
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        database=os.getenv('REDIS_DB', '0')
    )
    
    try:
        # Using context manager for automatic connection management
        with DatabaseConnection(config) as db:
            print("✅ Connected to Redis database")
            
            # Clean database for example
            db.execute("FLUSHDB")
            
            # String operations
            print("\n🔤 String Operations:")
            result = db.execute("SET username alice")
            print(f"SET username alice: {result.success}")
            
            result = db.execute("GET username")
            print(f"GET username: {result.rows[0][0] if result.rows else 'None'}")
            
            # Hash operations
            print("\n🗃️ Hash Operations:")
            result = db.execute("HSET user:1000 name John age 30 email john@example.com")
            print(f"HSET user:1000: {result.success}")
            
            result = db.execute("HGETALL user:1000")
            print(f"HGETALL user:1000: {dict(result.rows) if result.rows else {}}")
            
            # List operations
            print("\n📋 List Operations:")
            result = db.execute("LPUSH tasks 'task1' 'task2' 'task3'")
            print(f"LPUSH tasks: added {result.rows[0][0] if result.rows else 0} items")
            
            result = db.execute("LRANGE tasks 0 -1")
            print(f"LRANGE tasks: {[row[0] for row in result.rows]}")
            
            # Set operations
            print("\n🔢 Set Operations:")
            result = db.execute("SADD tags redis database nosql")
            print(f"SADD tags: added {result.rows[0][0] if result.rows else 0} items")
            
            result = db.execute("SMEMBERS tags")
            print(f"SMEMBERS tags: {[row[0] for row in result.rows]}")
            
            # Using method-based interface
            print("\n⚡ Method-based Operations:")
            adapter = db.execute._adapter
            
            # Set with expiration
            success = adapter.set("temp_key", "temp_value", ex=10)
            print(f"Set with expiration: {success}")
            
            # Check existence
            exists = adapter.exists("username")
            print(f"Key 'username' exists: {exists}")
            
            # Get keys pattern
            keys = adapter.keys("user*")
            print(f"Keys matching 'user*': {keys}")
            
            # Get Redis info
            info = adapter.info('server')
            print(f"Redis version: {info.get('redis_version', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ Redis operation failed: {e}")


if __name__ == "__main__":
    redis_example()