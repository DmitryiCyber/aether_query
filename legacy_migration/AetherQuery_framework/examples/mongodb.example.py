"""Example usage of MongoDB adapter"""

from python.aetherquery.db.connection import DatabaseConnection
from python.aetherquery.core.config import DatabaseConfig
import os


def check_mongodb_availability():
    """Check if MongoDB is available"""
    try:
        config = DatabaseConfig(
            type="mongodb",
            host=os.getenv('MONGODB_HOST', 'localhost'),
            port=int(os.getenv('MONGODB_PORT', 27017)),
            database=os.getenv('MONGODB_DB', 'test_db')
        )
        
        with DatabaseConnection(config) as db:
            return db.execute._adapter.test_connection()
    except Exception:
        return False


def mongodb_example():
    """Demonstrate MongoDB adapter usage"""
    
    if not check_mongodb_availability():
        print("❌ MongoDB is not available")
        print("💡 You can start MongoDB with Docker:")
        print("   docker run -d --name mongodb-test -p 27017:27017 mongo:6.0")
        return
    
    # Configuration for MongoDB
    config = DatabaseConfig(
        type="mongodb",
        host=os.getenv('MONGODB_HOST', 'localhost'),
        port=int(os.getenv('MONGODB_PORT', 27017)),
        database=os.getenv('MONGODB_DB', 'test_db')
    )
    
    try:
        # Using context manager for automatic connection management
        with DatabaseConnection(config) as db:
            print("✅ Connected to MongoDB database")
            
            # Create collection
            success = db.execute._adapter.create_collection("example_users")
            print(f"✅ Collection created: {success}")
            
            # Insert some data using native MongoDB syntax
            result = db.execute(
                "db.example_users.insert",
                {"documents": [
                    {
                        "username": "alice",
                        "email": "alice@example.com",
                        "age": 28,
                        "interests": ["programming", "reading"]
                    },
                    {
                        "username": "bob", 
                        "email": "bob@example.com",
                        "age": 32,
                        "interests": ["gaming", "music"]
                    },
                    {
                        "username": "charlie",
                        "email": "charlie@example.com", 
                        "age": 25,
                        "interests": ["sports", "travel"]
                    }
                ]}
            )
            print(f"✅ Inserted users: {result.row_count} documents")
            
            # Find data using native syntax
            result = db.execute(
                "db.example_users.find",
                {"filter": {}, "limit": 5}
            )
            print(f"\n✅ Query result: {result.row_count} users found")
            
            for row in result.rows:
                print(f"User: {dict(zip(result.columns, row))}")
            
            # Show collections
            collections = db.execute._adapter.get_collections()
            print(f"\n📋 Collections in database: {collections}")
            
            # Create index
            success = db.execute._adapter.create_index(
                "example_users", 
                [("email", 1)], 
                unique=True
            )
            print(f"✅ Email index created: {success}")
            
    except Exception as e:
        print(f"❌ MongoDB operation failed: {e}")


if __name__ == "__main__":
    mongodb_example()