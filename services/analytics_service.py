from datetime import datetime, timedelta
import streamlit as st


def log_user_activity(db, user_id, activity_type, target_type=None, target_id=None, details=None):
    """Log user activity to the database."""
    try:
        query = """
            INSERT INTO user_activities (user_id, activity_type, target_type, target_id, details, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        db.insert_data(query, (
            user_id,
            activity_type,
            target_type,
            target_id,
            details,
            datetime.now()
        ))
        
    except Exception as e:
        # Don't show error to user for logging failures
        print(f"Activity logging error: {e}")


def get_user_activity_stats(db, user_id, days=30):
    """Get user activity statistics for specified time period."""
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        query = """
            SELECT activity_type, COUNT(*) as count
            FROM user_activities 
            WHERE user_id = %s AND created_at >= %s
            GROUP BY activity_type
            ORDER BY count DESC
        """
        
        results = db.fetch_all(query, (user_id, start_date))
        return {row['activity_type']: row['count'] for row in results} if results else {}
        
    except Exception as e:
        st.error(f"Error fetching activity stats: {e}")
        return {}


def get_recent_user_activities(db, user_id, limit=10):
    """Get recent user activities."""
    try:
        query = """
            SELECT activity_type, target_type, target_id, details, created_at
            FROM user_activities 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        
        results = db.fetch_all(query, (user_id, limit))
        return results if results else []
        
    except Exception as e:
        st.error(f"Error fetching recent activities: {e}")
        return []


def get_daily_activity_count(db, user_id, days=7):
    """Get daily activity counts for the past N days."""
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        query = """
            SELECT DATE(created_at) as activity_date, COUNT(*) as count
            FROM user_activities 
            WHERE user_id = %s AND created_at >= %s
            GROUP BY DATE(created_at)
            ORDER BY activity_date DESC
        """
        
        results = db.fetch_all(query, (user_id, start_date))
        return {str(row['activity_date']): row['count'] for row in results} if results else {}
        
    except Exception as e:
        st.error(f"Error fetching daily activity: {e}")
        return {}


def get_activity_by_type(db, user_id, activity_type, limit=20):
    """Get specific type of activities for a user."""
    try:
        query = """
            SELECT target_type, target_id, details, created_at
            FROM user_activities 
            WHERE user_id = %s AND activity_type = %s
            ORDER BY created_at DESC 
            LIMIT %s
        """
        
        results = db.fetch_all(query, (user_id, activity_type, limit))
        return results if results else []
        
    except Exception as e:
        st.error(f"Error fetching activities by type: {e}")
        return []


# Activity type constants for consistency
class ActivityTypes:
    LOGIN = "login"
    LOGOUT = "logout"
    ITEM_ADDED = "item_added"
    ITEM_UPDATED = "item_updated"
    ITEM_DELETED = "item_deleted"
    OUTFIT_GENERATED = "outfit_generated"
    OUTFIT_SAVED = "outfit_saved"
    OUTFIT_DELETED = "outfit_deleted"
    CUSTOM_OUTFIT_CREATED = "custom_outfit_created"
    WARDROBE_VIEWED = "wardrobe_viewed"
    ANALYTICS_VIEWED = "analytics_viewed"
    RECOMMENDATIONS_VIEWED = "recommendations_viewed"


# Target type constants for consistency
class TargetTypes:
    WARDROBE_ITEM = "wardrobe_item"
    OUTFIT = "outfit"
    USER_PROFILE = "user_profile"
    DASHBOARD = "dashboard"
    WARDROBE = "wardrobe"
    GENERATOR = "generator"
    ANALYTICS = "analytics"
    RECOMMENDATIONS = "recommendations"


def log_login(db, user_id):
    """Convenience function to log user login."""
    log_user_activity(db, user_id, ActivityTypes.LOGIN, TargetTypes.USER_PROFILE)


def log_logout(db, user_id):
    """Convenience function to log user logout."""
    log_user_activity(db, user_id, ActivityTypes.LOGOUT, TargetTypes.USER_PROFILE)


def log_item_action(db, user_id, action, item_id, item_name=None):
    """Convenience function to log wardrobe item actions."""
    details = f"Item: {item_name}" if item_name else None
    log_user_activity(db, user_id, action, TargetTypes.WARDROBE_ITEM, item_id, details)


def log_outfit_action(db, user_id, action, outfit_id, outfit_name=None):
    """Convenience function to log outfit actions."""
    details = f"Outfit: {outfit_name}" if outfit_name else None
    log_user_activity(db, user_id, action, TargetTypes.OUTFIT, outfit_id, details)


def log_page_view(db, user_id, page_name):
    """Convenience function to log page views."""
    log_user_activity(db, user_id, f"{page_name}_viewed", page_name.upper())
