from typing import List, Dict, Optional
from database_config import db


class DataAccessLayer:
    """
    Database abstraction layer for LookBook V2 using PyMySQL connection.
    """

    def __init__(self):
        self.db = db

    def save_user_data(self, user_data: Dict) -> bool:
        """Save user data to database"""
        try:
            query = """
            INSERT INTO users (username, email, password) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            email = VALUES(email), password = VALUES(password)
            """
            result = self.db.insert_data(query, (
                user_data['username'],
                user_data['email'],
                user_data.get('password', '')   # ✅ use plain text password field
            ))
            return result is not None
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False

    def load_user_data(self, username: str) -> Optional[Dict]:
        """Load user data from database"""
        try:
            query = "SELECT * FROM users WHERE username = %s"
            result = self.db.fetch_one(query, (username,))
            return result
        except Exception as e:
            print(f"Error loading user data: {e}")
            return None

    def save_wardrobe_data(self, user_id: int, wardrobe_data: List[Dict]) -> bool:
        """Save wardrobe data to database"""
        try:
            # Clear existing items for this user
            delete_query = "DELETE FROM wardrobe_items WHERE user_id = %s"
            self.db.delete_data(delete_query, (user_id,))

            # Insert new items
            insert_query = """
            INSERT INTO wardrobe_items 
            (user_id, item_name, category, color, brand, size, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            for item in wardrobe_data:
                self.db.insert_data(insert_query, (
                    user_id, item.get('name', ''), item.get('category', ''),
                    item.get('color', ''), item.get('brand', ''),
                    item.get('size', ''), item.get('image_path', '')
                ))
            return True
        except Exception as e:
            print(f"Error saving wardrobe data: {e}")
            return False

    def load_wardrobe_data(self, user_id: int) -> List[Dict]:
        """Load wardrobe data from database"""
        try:
            query = "SELECT * FROM wardrobe_items WHERE user_id = %s"
            results = self.db.fetch_all(query, (user_id,))
            return results if results else []
        except Exception as e:
            print(f"Error loading wardrobe data: {e}")
            return []


# Global DAL instance
dal = DataAccessLayer()
