import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    try:
        # Connect to default 'postgres' database to create new db
        conn = psycopg2.connect(
            user="postgres", 
            password="iimadmin", 
            host="localhost", 
            port="5432",
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        db_name = "api_product_db"
        
        # Check if exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database {db_name}...")
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created successfully.")
        else:
            print(f"Database {db_name} already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        # Identify if it's an auth error or connection error
        if "password authentication failed" in str(e):
             print("\n!!! Authentication Failed. Please check DB_USERNAME and DB_PASSWORD.")

if __name__ == "__main__":
    create_db()
