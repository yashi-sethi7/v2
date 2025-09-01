import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """Unified PyMySQL connection and helper methods for LookBook V2"""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.database = os.getenv("DB_NAME", "lookbook_db")
        self.user = os.getenv("DB_USERNAME", "root")
        self.password = os.getenv("DB_PASSWORD", "root")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.connection = None

    def connect(self):
        """Establish a PyMySQL connection"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor,  # always return dictionaries
                autocommit=False
            )
            return True
        except pymysql.MySQLError as e:
            st.error(f"❌ Database connection failed: {e}")
            return False

    def get_connection(self):
        """Get an active connection, reconnect if needed"""
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            return self.connection
        except Exception:
            self.connect()
            return self.connection

    def close(self):
        """Close the DB connection"""
        if self.connection and self.connection.open:
            self.connection.close()

    # -----------------
    # HELPER METHODS
    # -----------------

    def fetch_one(self, query, params=None):
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        except Exception as e:
            st.error(f"Fetch one failed: {e}")
            return None

    def fetch_all(self, query, params=None):
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except Exception as e:
            st.error(f"Fetch all failed: {e}")
            return []

    def insert_data(self, query, params=None):
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Insert failed: {e}")
            return None

    def update_data(self, query, params=None):
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            st.error(f"Update failed: {e}")
            return 0

    def delete_data(self, query, params=None):
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            st.error(f"Delete failed: {e}")
            return 0


# Global database instance
db = DatabaseConnection()
