import pymysql
from pymysql import Error
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.database = os.getenv('DB_NAME', 'lookbook_db')
        self.user = os.getenv('DB_USER','root')
        self.password = os.getenv('DB_PASSWORD','root')
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            return self.connection
        except Error as e:
            st.error(f"Database connection error: {e}")
            return None

    def disconnect(self):
        if self.connection and self.connection.open:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor
        except Error as e:
            st.error(f"Query execution error: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        return None

    def insert_data(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        return None

    def update_data(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        return 0

    def delete_data(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        return 0

# Create global database instance
@st.cache_resource
def get_database():
    db = DatabaseConnection()
    db.connect()
    return db
