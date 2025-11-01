import sys
from sqlalchemy import create_engine
from pymongo import MongoClient
from dotenv import load_dotenv
import os

def test_postgres_connection():
    try:
        load_dotenv()
        engine = create_engine(os.getenv('DATABASE_URL'))
        conn = engine.connect()
        print("✅ PostgreSQL connection successful!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {str(e)}")
        return False

def test_mongodb_connection():
    try:
        load_dotenv()
        client = MongoClient(os.getenv('MONGODB_URI'))
        client.server_info()  # Test the connection
        print("✅ MongoDB connection successful!")
        print("   Available databases:", client.list_database_names())
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing database connections...\n")
    
    pg_success = test_postgres_connection()
    mongo_success = test_mongodb_connection()
    
    print("\nTest Summary:")
    print(f"PostgreSQL: {'✅ Success' if pg_success else '❌ Failed'}")
    print(f"MongoDB:    {'✅ Success' if mongo_success else '❌ Failed'}")
    
    if not (pg_success and mongo_success):
        sys.exit(1)