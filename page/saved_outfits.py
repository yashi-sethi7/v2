# import streamlit as st
# from PIL import Image
# import os
# from datetime import datetime

# class SavedOutfitsDatabase:
#     """Database operations for saved outfits management in V2"""

#     def __init__(self, db):
#         self.db = db

#     def get_user_saved_outfits(self, username: str) -> list:
#         try:
#             query = """
#                 SELECT 
#                     o.id as outfit_id, o.name as outfit_name, o.occasion, o.season,
#                     o.compatibility_score, o.created_at as saved_at,
#                     wi.id as item_id, wi.item_name, wi.category, wi.subcategory_id,
#                     wi.image_path
#                 FROM outfits o
#                 JOIN users u ON o.user_id = u.user_id
#                 JOIN outfit_items oi ON oi.outfit_id = o.id
#                 JOIN wardrobe_items wi ON wi.id = oi.wardrobe_item_id
#                 WHERE u.username = %s
#                 ORDER BY o.created_at DESC
#             """
#             results = self.db.fetch_all(query, (username,))

#             outfits = {}
#             for row in results:
#                 outfit_id = row['outfit_id']
#                 if outfit_id not in outfits:
#                     outfits[outfit_id] = {
#                         'outfit_id': outfit_id,
#                         'name': row['outfit_name'],
#                         'event': row['occasion'] or 'Unknown',
#                         'weather': row['season'] or 'Unknown',
#                         'day': self.extract_day_from_outfit_name(row['outfit_name']),
#                         'compatibility_score': row['compatibility_score'],
#                         'saved_at': row['saved_at'].isoformat() if row.get('saved_at') else datetime.now().isoformat(),
#                         'items': []
#                     }

#                 item = {
#                     'item_id': row['item_id'],
#                     'name': row['item_name'],
#                     'category': row['category'],
#                     'subcategory': row.get('subcategory_id') or 'Unknown',
#                     'image': row.get('image_path')
#                 }
#                 outfits[outfit_id]['items'].append(item)

#             return list(outfits.values())

#         except Exception as e:
#             st.error(f"Error loading saved outfits: {e}")
#             return []

#     def extract_day_from_outfit_name(self, outfit_name: str) -> str:
#         days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#         for day in days:
#             if day.lower() in outfit_name.lower():
#                 return day
#         return "Unknown Day"

#     def delete_saved_outfit(self, username: str, outfit_id: int) -> bool:
#         try:
#             verify = self.db.fetch_one("""
#                 SELECT o.id FROM outfits o
#                 JOIN users u ON o.user_id = u.user_id
#                 WHERE o.id = %s AND u.username = %s
#             """, (outfit_id, username))

#             if not verify:
#                 st.error("Outfit not found or access denied")
#                 return False

#             self.db.delete_data("DELETE FROM outfit_items WHERE outfit_id = %s", (outfit_id,))
#             deleted_rows = self.db.delete_data("DELETE FROM outfits WHERE id = %s", (outfit_id,))
#             return deleted_rows > 0
#         except Exception as e:
#             st.error(f"Error deleting outfit: {e}")
#             return False


# DAYS_OF_WEEK = [
#     "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
# ]

# EVENT_OPTIONS = [
#     "Casual", "Formal", "Comfortable", "Party", "Date", "Wedding", "Cocktail",
#     "Work", "Shopping", "Brunch", "Dinner", "Meeting", "Interview",
#     "Sport", "Gym", "Yoga", "Beach", "Vacation", "Home", "Festival", "Concert",
#     "Theater", "Picnic", "Birthday", "Graduation"
# ]

# WEATHER_OPTIONS = [
#     "Hot", "Cold", "Freezing", "Mild", "Rainy", "Windy", "Sunny", "Cloudy",
#     "Snowy", "Stormy", "Humid", "Dry"
# ]

# def display_saved_item(item):
#     if item.get("image") and os.path.exists(item["image"]):
#         try:
#             img = Image.open(item["image"])
#             img = img.resize((145, 193), Image.Resampling.LANCZOS)
#             st.image(img)
#         except:
#             st.write("📷 Image error")
#     else:
#         st.write("📷 No image")

# def saved_outfits_page(db):
#     global saved_outfits_db
#     saved_outfits_db = SavedOutfitsDatabase(db)

#     st.markdown("<h1 style='font-size:2rem; font-weight:700;'>💾 Your Saved Outfits</h1>", unsafe_allow_html=True)

#     username = st.session_state.username
#     outfits = saved_outfits_db.get_user_saved_outfits(username)

#     if not outfits:
#         st.info("You have no saved outfits yet.")
#         return

#     with st.sidebar:
#         st.markdown("<h3>Filters</h3>", unsafe_allow_html=True)
#         day_filter = st.selectbox("Day of Week", ["All"] + DAYS_OF_WEEK)
#         weather_filter = st.selectbox("Weather", ["All"] + WEATHER_OPTIONS)
#         event_filter = st.selectbox("Event", ["All"] + EVENT_OPTIONS)
#         sort_option = st.selectbox("Sort by", ["Newest First", "Oldest First", "Compatibility"])

#     filtered = outfits

#     if day_filter != "All":
#         filtered = [o for o in filtered if o["day"] == day_filter]

#     if weather_filter != "All":
#         filtered = [o for o in filtered if o.get("weather") == weather_filter]

#     if event_filter != "All":
#         filtered = [o for o in filtered if o.get("event") == event_filter]

#     if sort_option == "Newest First":
#         filtered.sort(key=lambda x: x.get("saved_at", ""), reverse=True)
#     elif sort_option == "Oldest First":
#         filtered.sort(key=lambda x: x.get("saved_at", ""))
#     elif sort_option == "Compatibility":
#         filtered.sort(key=lambda x: x.get("compatibility_score", 0), reverse=True)

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Saved Outfits", len(outfits))
#     col2.metric("Showing", len(filtered))
#     unique_days = len(set(o.get("day") for o in outfits))
#     col3.metric("Days Planned", unique_days)

#     st.markdown("---")

#     for outfit in filtered:
#         st.markdown(f"### {outfit['day']} Outfit")
#         st.markdown(f"**Event:** {outfit.get('event')}  |  **Weather:** {outfit.get('weather')}")
#         st.markdown(f"**Compatibility:** {outfit.get('compatibility_score')}%")
#         saved_date = outfit.get("saved_at", "")
#         if saved_date:
#             try:
#                 saved_date_fmt = datetime.fromisoformat(saved_date).strftime("%b %d, %Y %I:%M %p")
#                 st.markdown(f"*Saved on: {saved_date_fmt}*")
#             except:
#                 pass

#         col1, col2, col3 = st.columns([3, 1, 1])
#         if col3.button(f"Delete {outfit['name']}", key=f"delete_{outfit['outfit_id']}"):
#             if saved_outfits_db.delete_saved_outfit(username, outfit['outfit_id']):
#                 st.success("Outfit deleted.")
#                 st.experimental_rerun()
#             else:
#                 st.error("Failed to delete outfit.")

#         items = outfit.get("items", [])
#         cols = st.columns(len(items))
#         for i, item in enumerate(items):
#             with cols[i]:
#                 display_saved_item(item)
#                 st.caption(item.get("name", "Unknown"))
#                 st.caption(item.get("subcategory", ""))

#         st.markdown("---")


# if __name__ == "__main__":
#     from config.database import get_database
#     db = get_database()
#     saved_outfits_page(db)

import streamlit as st
from PIL import Image
import os
from datetime import datetime


class SavedOutfitsDatabase:
    """Database operations for saved outfits management in V2"""

    def __init__(self, db):
        self.db = db

    def get_user_saved_outfits(self, username: str) -> list:
        try:
            query = """
                SELECT 
                    o.id as outfit_id, o.name as outfit_name, o.occasion, o.season,
                    o.compatibility_score, o.created_at as saved_at,
                    wi.id as item_id, wi.name as item_name, wi.category, wi.subcategory,
                    wi.image_path
                FROM outfits o
                JOIN users u ON o.user_id = u.user_id
                JOIN outfit_items oi ON oi.outfit_id = o.id
                JOIN wardrobe_items wi ON wi.id = oi.wardrobe_item_id
                WHERE u.username = %s
                ORDER BY o.created_at DESC
            """
            results = self.db.fetch_all(query, (username,))

            outfits = {}
            for row in results:
                outfit_id = row['outfit_id']
                if outfit_id not in outfits:
                    outfits[outfit_id] = {
                        'outfit_id': outfit_id,
                        'name': row['outfit_name'],
                        'event': row['occasion'] or 'Unknown',
                        'weather': row['season'] or 'Unknown',
                        'day': self.extract_day_from_outfit_name(row['outfit_name']),
                        'compatibility_score': row['compatibility_score'],
                        'saved_at': row['saved_at'].isoformat() if row.get('saved_at') else datetime.now().isoformat(),
                        'items': []
                    }

                item = {
                    'item_id': row['item_id'],
                    'name': row['item_name'],  # FIXED: Use 'item_name' from aliased query
                    'category': row['category'],
                    'subcategory': row.get('subcategory') or 'Unknown',  # FIXED: Use 'subcategory' not 'subcategory_id'
                    'image': row.get('image_path')
                }
                outfits[outfit_id]['items'].append(item)

            return list(outfits.values())

        except Exception as e:
            st.error(f"Error loading saved outfits: {e}")
            return []

    def extract_day_from_outfit_name(self, outfit_name: str) -> str:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            if day.lower() in outfit_name.lower():
                return day
        return "Unknown Day"

    def delete_saved_outfit(self, username: str, outfit_id: int) -> bool:
        try:
            verify = self.db.fetch_one("""
                SELECT o.id FROM outfits o
                JOIN users u ON o.user_id = u.user_id
                WHERE o.id = %s AND u.username = %s
            """, (outfit_id, username))

            if not verify:
                st.error("Outfit not found or access denied")
                return False

            self.db.delete_data("DELETE FROM outfit_items WHERE outfit_id = %s", (outfit_id,))
            deleted_rows = self.db.delete_data("DELETE FROM outfits WHERE id = %s", (outfit_id,))
            return deleted_rows > 0
        except Exception as e:
            st.error(f"Error deleting outfit: {e}")
            return False


DAYS_OF_WEEK = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

EVENT_OPTIONS = [
    "Casual", "Formal", "Comfortable", "Party", "Date", "Wedding", "Cocktail",
    "Work", "Shopping", "Brunch", "Dinner", "Meeting", "Interview",
    "Sport", "Gym", "Yoga", "Beach", "Vacation", "Home", "Festival", "Concert",
    "Theater", "Picnic", "Birthday", "Graduation"
]

WEATHER_OPTIONS = [
    "Hot", "Cold", "Freezing", "Mild", "Rainy", "Windy", "Sunny", "Cloudy",
    "Snowy", "Stormy", "Humid", "Dry"
]

# Add the matching sidebar theme CSS from wardrobe page
st.markdown("""
<style>
    /* Hide the problematic sidebar collapse button */
    .stSidebar > div > div > button {
        display: none !important;
    }
    
    /* Hide keyboard_left_arrow text in sidebar */
    .stSidebar [data-testid="stMarkdownContainer"] p:contains("keyboard_arrow_left"),
    .stSidebar [data-testid="stMarkdownContainer"]:has-text("keyboard_arrow_left") {
        display: none !important;
    }
    
    /* More comprehensive hiding of the arrow text */
    .stSidebar *:contains("keyboard_arrow_left") {
        display: none !important;
    }
    
    /* Sidebar background gradient - SAME AS WARDROBE PAGE */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;
    }
    
    /* Additional styling for consistency */
    .css-1d391kg {
        background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;
    }
    
    /* Style for saved outfit cards */
    .saved-outfit-card {
        background: #fefcfa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e8ddd4;
        box-shadow: 0 2px 8px rgba(212, 178, 158, 0.1);
    }
    
    /* Outfit header styling */
    .outfit-header {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #4a2511;
        margin-bottom: 0.5em;
    }
    
    /* Metrics styling */
    .stMetric {
        background: #faf8f5;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f0ebe5;
    }
</style>
""", unsafe_allow_html=True)

def display_saved_item(item):
    if item.get("image") and os.path.exists(item["image"]):
        try:
            img = Image.open(item["image"])
            img = img.resize((145, 193), Image.Resampling.LANCZOS)
            st.image(img)
        except:
            st.write("📷 Image error")
    else:
        st.write("📷 No image")

def saved_outfits_page(db):
    global saved_outfits_db
    saved_outfits_db = SavedOutfitsDatabase(db)

    st.markdown("---")
    st.markdown("""
        <h1 style='font-size:2.25rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        💾 Your Saved Outfits
        </h1>
    """, unsafe_allow_html=True)

    username = st.session_state.username
    outfits = saved_outfits_db.get_user_saved_outfits(username)

    if not outfits:
        st.info("🎨 You have no saved outfits yet. Create some outfits using the Generator to save them here!")
        return

    with st.sidebar:
        # Apply the same sidebar styling as wardrobe page
        st.markdown("""<style>.css-1d391kg {
        background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;}
        section[data-testid="stSidebar"] > div {
        background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;}
        </style>""", unsafe_allow_html=True)

        st.markdown("""<h1 style='font-size:1.35rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🔍 Filter & Sort</h1>""", unsafe_allow_html=True)
        
        st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        📅 Day Filter</h1>""", unsafe_allow_html=True)
        day_filter = st.selectbox("", ["All"] + DAYS_OF_WEEK, key="day_filter", label_visibility='collapsed')
        
        st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🌤️ Weather Filter</h1>""", unsafe_allow_html=True)
        weather_filter = st.selectbox("", ["All"] + WEATHER_OPTIONS, key="weather_filter", label_visibility='collapsed')
        
        st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🎭 Event Filter</h1>""", unsafe_allow_html=True)
        event_filter = st.selectbox("", ["All"] + EVENT_OPTIONS, key="event_filter", label_visibility='collapsed')
        
        st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        📊 Sort By</h1>""", unsafe_allow_html=True)
        sort_option = st.selectbox("", ["Newest First", "Oldest First", "Compatibility"], key="sort_filter", label_visibility='collapsed')

    # Apply filters
    filtered = outfits

    if day_filter != "All":
        filtered = [o for o in filtered if o["day"] == day_filter]

    if weather_filter != "All":
        filtered = [o for o in filtered if o.get("weather") == weather_filter]

    if event_filter != "All":
        filtered = [o for o in filtered if o.get("event") == event_filter]

    # Apply sorting
    if sort_option == "Newest First":
        filtered.sort(key=lambda x: x.get("saved_at", ""), reverse=True)
    elif sort_option == "Oldest First":
        filtered.sort(key=lambda x: x.get("saved_at", ""))
    elif sort_option == "Compatibility":
        filtered.sort(key=lambda x: x.get("compatibility_score", 0), reverse=True)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Saved Outfits", len(outfits))
    col2.metric("Showing", len(filtered))
    unique_days = len(set(o.get("day") for o in outfits))
    col3.metric("Days Planned", unique_days)

    st.markdown("---")

    # Display filtered outfits
    if not filtered:
        st.info("🔍 No outfits match your current filters. Try adjusting your filter settings.")
        return

    for outfit in filtered:
        # Create styled outfit card
        st.markdown('<div class="saved-outfit-card">', unsafe_allow_html=True)
        
        # Outfit header with improved styling
        col_header, col_delete = st.columns([4, 1])
        with col_header:
            st.markdown(f'<div class="outfit-header">👗 {outfit.get("name", "Unnamed Outfit")}</div>', unsafe_allow_html=True)
            
            # Outfit metadata
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                st.markdown(f"**📅 Day:** {outfit.get('day')}")
                st.markdown(f"**🎭 Event:** {outfit.get('event')}")
            with col_meta2:
                st.markdown(f"**🌤️ Weather:** {outfit.get('weather')}")
                st.markdown(f"**🎯 Match:** {outfit.get('compatibility_score')}%")
            
            # Saved date
            saved_date = outfit.get("saved_at", "")
            if saved_date:
                try:
                    saved_date_fmt = datetime.fromisoformat(saved_date).strftime("%b %d, %Y %I:%M %p")
                    st.caption(f"💾 Saved on: {saved_date_fmt}")
                except:
                    pass

        with col_delete:
            if st.button(f"🗑️ Delete", key=f"delete_{outfit['outfit_id']}", 
                        help="Delete this saved outfit", use_container_width=True):
                if saved_outfits_db.delete_saved_outfit(username, outfit['outfit_id']):
                    st.success("Outfit deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete outfit.")

        # Display outfit items
        items = outfit.get("items", [])
        if items:
            st.markdown("**Items in this outfit:**")
            cols = st.columns(min(len(items), 5))  # Max 5 columns
            for i, item in enumerate(items):
                with cols[i % 5]:
                    display_saved_item(item)
                    st.caption(f"**{item.get('name', 'Unknown')}**")
                    st.caption(f"{item.get('category', '')} • {item.get('subcategory', '')}")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")


if __name__ == "__main__":
    from config.database import get_database
    db = get_database()
    saved_outfits_page(db)
