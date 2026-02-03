"""Setup PostgreSQL database"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import getpass

print("🔧 PostgreSQL Database Setup")
print("=" * 50)

# Get database credentials
db_user = input("Enter PostgreSQL username [postgres]: ").strip() or "postgres"
db_password = getpass.getpass("Enter PostgreSQL password: ")
db_host = input("Enter PostgreSQL host [localhost]: ").strip() or "localhost"
db_port = input("Enter PostgreSQL port [5432]: ").strip() or "5432"
db_name = "foodorder_db"

# Create connection to postgres database (to create our database)
try:
    admin_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
    engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    
    with engine.connect() as conn:
        # Drop database if exists
        print(f"\n🗑️  Dropping database '{db_name}' if exists...")
        conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        
        # Create database
        print(f"📦 Creating database '{db_name}'...")
        conn.execute(text(f"CREATE DATABASE {db_name}"))
        
    print(f"✅ Database '{db_name}' created successfully!")
    
    # Update .env file
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    print(f"\n📝 Updating .env file...")
    
    env_content = f"""# Environment variables for database connection
# PostgreSQL database configuration
DATABASE_URL={database_url}
SECRET_KEY=dev-secret-key-12345
JWT_SECRET_KEY=jwt-secret-key-12345
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file updated!")
    print(f"\n🔑 Database URL: {database_url}")
    print("\nNext steps:")
    print("1. Run: python init_db.py (to create tables)")
    print("2. Run: python simple_seed.py (to add sample data)")
    print("3. Restart the Flask server")
    
except OperationalError as e:
    print(f"\n❌ Error: {e}")
    print("\nPlease check:")
    print("- PostgreSQL is running")
    print("- Username and password are correct")
    print("- PostgreSQL is accessible on the specified host and port")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    sys.exit(1)
