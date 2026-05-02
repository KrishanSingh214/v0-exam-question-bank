import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "question_bank")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "")
    
    def connect(self):
        """Connect to the database"""
        try:
            self.connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("Database connected successfully")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database disconnected")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
    
    def execute_single(self, query, params=None):
        """Execute a query that returns a single row"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
    
    def execute_insert(self, query, params=None):
        """Execute an INSERT query and return the ID"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone() if self.cursor.description else None
        except Exception as e:
            self.connection.rollback()
            print(f"Error inserting data: {e}")
            raise
    
    def execute_update(self, query, params=None):
        """Execute an UPDATE or DELETE query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating data: {e}")
            raise
    
    def execute_script(self, script_path):
        """Execute SQL script from file"""
        try:
            with open(script_path, 'r') as f:
                sql_script = f.read()
            self.cursor.execute(sql_script)
            self.connection.commit()
            print(f"SQL script {script_path} executed successfully")
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing script: {e}")
            raise

# Global database instance
db = Database()

def get_db():
    """Dependency for FastAPI to get database connection"""
    if not db.connection:
        db.connect()
    return db
