import re
from datetime import datetime
import streamlit as st

def validate_password(password):
    """Validate password meets security requirements."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def authenticate_user(db, username, password):
    """Authenticate user against database with plain text password."""
    try:
        query = "SELECT user_id, username, password FROM users WHERE username = %s"
        result = db.fetch_one(query, (username,))
        
        # Simple password comparison (no hashing)
        if result and result[2] == password:
            return {
                'user_id': result[0],
                'username': result[1]
            }
        return None
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return None

def create_user(db, username, password):
    """Create new user in database with plain text password."""
    try:
        # Check if username already exists
        check_query = "SELECT username FROM users WHERE username = %s"
        existing = db.fetch_one(check_query, (username,))
        
        if existing:
            return False, "Username already exists. Please choose a different username.", None
        
        # Store password as plain text (no hashing)
        insert_query = """
            INSERT INTO users (username, password, created_at, updated_at) 
            VALUES (%s, %s, %s, %s)
        """
        
        now = datetime.now()
        user_id = db.insert_data(insert_query, (username, password, now, now))
        
        if user_id:
            return True, "User created successfully!", user_id
        else:
            return False, "Failed to create user. Please try again.", None
            
    except Exception as e:
        st.error(f"User creation error: {e}")
        return False, f"Error creating user: {str(e)}", None

def get_user_by_id(db, user_id):
    """Get user details by user ID."""
    try:
        query = "SELECT user_id, username, created_at FROM users WHERE user_id = %s"
        result = db.fetch_one(query, (user_id,))
        
        if result:
            return {
                'user_id': result[0],
                'username': result[1],
                'created_at': result[2]
            }
        return None
    except Exception as e:
        st.error(f"Error fetching user: {e}")
        return None
