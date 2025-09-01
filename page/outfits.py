# import streamlit as st
# from PIL import Image
# import os
# from datetime import datetime

# class OutfitManagementDatabase:
#     """Database operations for custom outfit creation and management"""

#     def __init__(self, db):
#         self.db = db

#     def get_user_wardrobe_for_selection(self, username: str) -> list:
#         query = """
#             SELECT wi.*, u.username 
#             FROM wardrobe_items wi 
#             JOIN users u ON wi.user_id = u.user_id 
#             WHERE u.username = %s 
#             ORDER BY wi.category, wi.name
#         """
#         try:
#             items = self.db.fetch_all(query, (username,))
#             formatted_items = []
#             for item in items:
#                 formatted_items.append({
#                     'item_id': item.get('id'),  # PK column is 'id'
#                     'name': item.get('name', 'Unknown Item'),  # Fixed: use 'name' column
#                     'category': item.get('category', 'Uncategorized'),
#                     'subcategory': item.get('subcategory', ''),  # Fixed: use 'subcategory' not 'subcategory_id'
#                     'image': item.get('image_path', '')
#                 })
#             return formatted_items
#         except Exception as e:
#             st.error(f"Error loading wardrobe: {str(e)}")
#             return []

#     def create_custom_outfit(self, username, outfit_name, description="", weather_condition="",
#                             event_type="", day_of_week="", date_created=None, last_worn=None,
#                             compatibility_score=0, occasion="", season="", selected_items=None):
#         if selected_items is None:
#             selected_items = []
#         try:
#             user_result = self.db.fetch_one("SELECT user_id FROM users WHERE username = %s", (username,))
#             if not user_result:
#                 st.error("User not found")
#                 return False
#             user_id = user_result['user_id']
#             insert_query = """
#                 INSERT INTO outfits (
#                     user_id, name, description, weather_condition, event_type, day_of_week, 
#                     date_created, last_worn, compatibility_score, occasion, season
#                 )
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             outfit_id = self.db.insert_data(insert_query, (
#                 user_id, outfit_name, description, weather_condition, event_type, day_of_week,
#                 date_created, last_worn, compatibility_score, occasion, season
#             ))
#             if not outfit_id:
#                 st.error("Failed to create outfit record")
#                 return False
#             # Insert outfit items linking with wardrobe_item_id
#             for item_id in selected_items:
#                 try:
#                     self.db.insert_data(
#                         "INSERT INTO outfit_items (outfit_id, wardrobe_item_id) VALUES (%s, %s)", (outfit_id, item_id)
#                     )
#                 except Exception as item_err:
#                     st.error(f"Error adding item {item_id} to outfit: {item_err}")
#             return True
#         except Exception as e:
#             st.error(f"Error creating outfit: {str(e)}")
#             return False

#     def get_user_custom_outfits(self, username: str):
#         query = """
#             SELECT 
#                 o.id as outfit_id, o.name, o.description, o.weather_condition, o.event_type, o.day_of_week,
#                 o.date_created, o.last_worn, o.created_at, o.updated_at, o.compatibility_score, o.occasion, o.season,
#                 wi.id as item_id, wi.name as item_name, wi.category, wi.subcategory,
#                 wi.image_path
#             FROM outfits o
#             JOIN users u ON o.user_id = u.user_id
#             JOIN outfit_items oi ON o.id = oi.outfit_id
#             JOIN wardrobe_items wi ON oi.wardrobe_item_id = wi.id
#             WHERE u.username = %s
#             ORDER BY o.created_at DESC
#         """
#         try:
#             results = self.db.fetch_all(query, (username,))
#             if not results:
#                 return []
#             outfits_dict = {}
#             for row in results:
#                 outfit_id = row.get('outfit_id')
#                 if outfit_id not in outfits_dict:
#                     outfits_dict[outfit_id] = {
#                         'outfit_id': outfit_id,
#                         'name': row.get('name', 'Unnamed Outfit'),
#                         'description': row.get('description', ''),
#                         'weather_condition': row.get('weather_condition', ''),
#                         'event_type': row.get('event_type', ''),
#                         'day_of_week': row.get('day_of_week', ''),
#                         'date_created': row.get('date_created', ''),
#                         'last_worn': row.get('last_worn', ''),
#                         'created_at': row.get('created_at', ''),
#                         'updated_at': row.get('updated_at', ''),
#                         'compatibility_score': row.get('compatibility_score', 0),
#                         'occasion': row.get('occasion', ''),
#                         'season': row.get('season', ''),
#                         'items': []
#                     }
#                 item = {
#                     'item_id': row.get('item_id'),
#                     'name': row.get('item_name', 'Unknown Item'),  # Fixed: use aliased column name
#                     'category': row.get('category', 'Unknown'),
#                     'subcategory': row.get('subcategory', 'Unknown'),  # Fixed: use 'subcategory'
#                     'image': row.get('image_path', '')
#                 }
#                 outfits_dict[outfit_id]['items'].append(item)
#             return list(outfits_dict.values())
#         except Exception as e:
#             st.error(f"Error loading custom outfits: {str(e)}")
#             return []


# CATEGORIES = [
#     "Shirt", "T-shirt", "Jeans", "Jacket", "Sneakers", "Dress", "Tops",
#     "Bottoms", "Outerwear", "Shoes", "Accessories", "Activewear", "Swimwear", "Sleepwear"
# ]


# def display_outfit_item_thumbnail(item, size=100):
#     try:
#         if item.get("image") and os.path.exists(item["image"]):
#             img = Image.open(item["image"])
#             return img.resize((size, size), Image.Resampling.LANCZOS)
#         return Image.new('RGB', (size, size), color=(245, 241, 236))
#     except Exception:
#         return Image.new('RGB', (size, size), color=(245, 241, 236))


# def outfit_creation_interface(username: str):
#     wardrobe_items = outfit_mgmt_db.get_user_wardrobe_for_selection(username)
#     if not wardrobe_items:
#         st.warning("📭 Add items to your wardrobe first to create outfits!")
#         return

#     # Initialize selected items in session state
#     if 'selected_items' not in st.session_state:
#         st.session_state.selected_items = set()

#     # Item selection interface OUTSIDE the form
#     st.markdown("### 🛒 Select Items for Your Outfit")
#     items_by_category = {}
#     for item in wardrobe_items:
#         category = item.get('category', 'Other')
#         items_by_category.setdefault(category, []).append(item)
    
#     for category in CATEGORIES:
#         if category in items_by_category:
#             st.markdown(f"**{category}**")
#             cols = st.columns(min(len(items_by_category[category]), 5))
#             for idx, item in enumerate(items_by_category[category]):
#                 with cols[idx % 5]:
#                     item_id = item.get('item_id')
#                     if not item_id:
#                         continue
#                     is_selected = item_id in st.session_state.selected_items
#                     thumbnail = display_outfit_item_thumbnail(item)
#                     item_name = item.get('name', 'Unknown Item')
#                     display_name = f"{item_name[:15]}..." if len(item_name) > 15 else item_name
                    
#                     # Selection button
#                     if st.button(
#                         display_name,
#                         key=f"select_{item_id}",
#                         help=f"Click to {'remove' if is_selected else 'add'} {item_name}"
#                     ):
#                         if is_selected:
#                             st.session_state.selected_items.discard(item_id)
#                         else:
#                             st.session_state.selected_items.add(item_id)
#                         st.rerun()
                    
#                     if is_selected:
#                         st.success("✓ Selected")
#                     st.image(thumbnail, width=80)

#     # Display selected items count
#     selected_count = len(st.session_state.selected_items)
#     if selected_count > 0:
#         st.info(f"✅ {selected_count} item(s) selected for this outfit")
#     else:
#         st.warning("⚠️ Please select at least one item for your outfit")

#     # Form for outfit details
#     with st.form("outfit_form", clear_on_submit=True):
#         st.markdown("### 📝 Outfit Details")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             name = st.text_input("Outfit Name *", placeholder="e.g., Casual Friday Look")
#             description = st.text_area("Description", placeholder="Brief description of the outfit...")
#             occasion = st.text_input("Occasion", placeholder="e.g., Work, Party, Date")
#             season = st.text_input("Season", placeholder="e.g., Summer, Winter")
            
#         with col2:
#             weather_condition = st.text_input("Weather Condition", placeholder="e.g., Sunny, Rainy")
#             event_type = st.text_input("Event Type", placeholder="e.g., Formal, Casual")
#             day_of_week = st.text_input("Day of Week", placeholder="e.g., Monday, Weekend")
#             compatibility_score = st.number_input("Compatibility Score", min_value=0, max_value=100, value=70)
            
#         col3, col4 = st.columns(2)
#         with col3:
#             date_created = st.date_input("Date Created", value=datetime.today())
#         with col4:
#             last_worn = st.date_input("Last Worn", value=datetime.today())

#         # Submit button
#         submitted = st.form_submit_button("🎨 Create Outfit", use_container_width=True)
        
#         if submitted:
#             if not name.strip():
#                 st.error("Please enter an outfit name.")
#                 return
            
#             if not st.session_state.selected_items:
#                 st.error("Please select at least one item for your outfit.")
#                 return
                
#             success = outfit_mgmt_db.create_custom_outfit(
#                 username, name.strip(), description.strip(),
#                 weather_condition.strip(), event_type.strip(), day_of_week.strip(),
#                 str(date_created), str(last_worn),
#                 int(compatibility_score), occasion.strip(), season.strip(),
#                 list(st.session_state.selected_items)
#             )
#             if success:
#                 st.success("🎉 Custom outfit created successfully!")
#                 st.session_state.selected_items = set()  # Clear selections
#                 st.rerun()
#             else:
#                 st.error("Failed to create outfit. Please try again.")


# def display_custom_outfits(username: str):
#     custom_outfits = outfit_mgmt_db.get_user_custom_outfits(username)
#     if not custom_outfits:
#         st.info("🎨 No custom outfits yet. Create your first one above!")
#         return
    
#     st.markdown("---")
#     st.markdown("## 🧷 Your Custom Outfits")
    
#     for outfit in custom_outfits:
#         st.markdown("---")
        
#         # Outfit header
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             st.markdown(f"### {outfit.get('name', 'Unnamed Outfit')}")
#         with col2:
#             st.markdown(f"**Score: {outfit.get('compatibility_score', 0)}/100**")
        
#         # Outfit details
#         if outfit.get('description'):
#             st.markdown(f"**Description:** {outfit.get('description')}")
        
#         # Outfit metadata in columns
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             if outfit.get('weather_condition'):
#                 st.markdown(f"🌤️ **Weather:** {outfit.get('weather_condition')}")
#             if outfit.get('occasion'):
#                 st.markdown(f"🎯 **Occasion:** {outfit.get('occasion')}")
#         with col2:
#             if outfit.get('event_type'):
#                 st.markdown(f"🎪 **Event:** {outfit.get('event_type')}")
#             if outfit.get('season'):
#                 st.markdown(f"🍂 **Season:** {outfit.get('season')}")
#         with col3:
#             if outfit.get('day_of_week'):
#                 st.markdown(f"📅 **Day:** {outfit.get('day_of_week')}")
#             if outfit.get('last_worn'):
#                 st.markdown(f"👔 **Last Worn:** {outfit.get('last_worn')}")
        
#         # Creation/update info
#         if outfit.get('created_at'):
#             st.caption(f"Created: {outfit.get('created_at')} | Updated: {outfit.get('updated_at', 'Never')}")
        
#         # Outfit items
#         items = outfit.get('items', [])
#         if items:
#             st.markdown("**Items in this outfit:**")
#             cols = st.columns(min(len(items), 5))
#             for idx, item in enumerate(items):
#                 with cols[idx % 5]:
#                     image_path = item.get("image", "")
#                     if image_path and os.path.exists(image_path):
#                         img = Image.open(image_path)
#                         st.image(img, width=100)
#                     else:
#                         st.markdown(
#                             "<div style='width:100px; height:100px; background:#f0f0f0; "
#                             "display:flex; align-items:center; justify-content:center; "
#                             "border-radius:8px;'>📷</div>", 
#                             unsafe_allow_html=True
#                         )
#                     st.caption(f"**{item.get('name')}**")
#                     st.caption(f"{item.get('category')} • {item.get('subcategory')}")


# def outfits_page(db):
#     """Main outfits page function"""
#     global outfit_mgmt_db
#     outfit_mgmt_db = OutfitManagementDatabase(db)
#     username = st.session_state.username
    
#     st.markdown("---")
#     st.markdown("""
#         <h1 style='font-size:2.55rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
#         🧷 Custom Outfits
#         </h1>
#     """, unsafe_allow_html=True)
    
#     outfit_creation_interface(username)
#     display_custom_outfits(username)


# if __name__ == "__main__":
#     from config.database import get_database
#     db = get_database()
#     outfits_page(db)

import streamlit as st
from PIL import Image
import os
from datetime import datetime

class OutfitManagementDatabase:
    """Database operations for custom outfit creation and management"""
    def __init__(self, db):
        self.db = db

    def get_user_wardrobe_for_selection(self, username: str) -> list:
        query = """
            SELECT wi.*, u.username 
            FROM wardrobe_items wi 
            JOIN users u ON wi.user_id = u.user_id 
            WHERE u.username = %s 
            ORDER BY wi.category, wi.name
        """
        try:
            items = self.db.fetch_all(query, (username,))
            formatted_items = []
            for item in items:
                formatted_items.append({
                    'item_id': item.get('id'),  # PK column is 'id'
                    'name': item.get('name', 'Unknown Item'),  # Fixed: use 'name' column
                    'category': item.get('category', 'Uncategorized'),
                    'subcategory': item.get('subcategory', ''),  # Fixed: use 'subcategory' not 'subcategory_id'
                    'image': item.get('image_path', '')
                })
            return formatted_items
        except Exception as e:
            st.error(f"Error loading wardrobe: {str(e)}")
            return []

    def create_custom_outfit(self, username, outfit_name, description="", weather_condition="",
                            event_type="", day_of_week="", date_created=None, last_worn=None,
                            compatibility_score=0, occasion="", season="", selected_items=None):
        if selected_items is None:
            selected_items = []
        try:
            user_result = self.db.fetch_one("SELECT user_id FROM users WHERE username = %s", (username,))
            if not user_result:
                st.error("User not found")
                return False
            user_id = user_result['user_id']

            insert_query = """
                INSERT INTO outfits (
                    user_id, name, description, weather_condition, event_type, day_of_week, 
                    date_created, last_worn, compatibility_score, occasion, season
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            outfit_id = self.db.insert_data(insert_query, (
                user_id, outfit_name, description, weather_condition, event_type, day_of_week,
                date_created, last_worn, compatibility_score, occasion, season
            ))

            if not outfit_id:
                st.error("Failed to create outfit record")
                return False

            # Insert outfit items linking with wardrobe_item_id
            for item_id in selected_items:
                try:
                    self.db.insert_data(
                        "INSERT INTO outfit_items (outfit_id, wardrobe_item_id) VALUES (%s, %s)", (outfit_id, item_id)
                    )
                except Exception as item_err:
                    st.error(f"Error adding item {item_id} to outfit: {item_err}")

            return True
        except Exception as e:
            st.error(f"Error creating outfit: {str(e)}")
            return False

    def get_user_custom_outfits(self, username: str):
        query = """
            SELECT 
                o.id as outfit_id, o.name, o.description, o.weather_condition, o.event_type, o.day_of_week,
                o.date_created, o.last_worn, o.created_at, o.updated_at, o.compatibility_score, o.occasion, o.season,
                wi.id as item_id, wi.name as item_name, wi.category, wi.subcategory,
                wi.image_path
            FROM outfits o
            JOIN users u ON o.user_id = u.user_id
            JOIN outfit_items oi ON o.id = oi.outfit_id
            JOIN wardrobe_items wi ON oi.wardrobe_item_id = wi.id
            WHERE u.username = %s
            ORDER BY o.created_at DESC
        """
        try:
            results = self.db.fetch_all(query, (username,))
            if not results:
                return []

            outfits_dict = {}
            for row in results:
                outfit_id = row.get('outfit_id')
                if outfit_id not in outfits_dict:
                    outfits_dict[outfit_id] = {
                        'outfit_id': outfit_id,
                        'name': row.get('name', 'Unnamed Outfit'),
                        'description': row.get('description', ''),
                        'weather_condition': row.get('weather_condition', ''),
                        'event_type': row.get('event_type', ''),
                        'day_of_week': row.get('day_of_week', ''),
                        'date_created': row.get('date_created', ''),
                        'last_worn': row.get('last_worn', ''),
                        'created_at': row.get('created_at', ''),
                        'updated_at': row.get('updated_at', ''),
                        'compatibility_score': row.get('compatibility_score', 0),
                        'occasion': row.get('occasion', ''),
                        'season': row.get('season', ''),
                        'items': []
                    }

                item = {
                    'item_id': row.get('item_id'),
                    'name': row.get('item_name', 'Unknown Item'),  # Fixed: use aliased column name
                    'category': row.get('category', 'Unknown'),
                    'subcategory': row.get('subcategory', 'Unknown'),  # Fixed: use 'subcategory'
                    'image': row.get('image_path', '')
                }
                outfits_dict[outfit_id]['items'].append(item)

            return list(outfits_dict.values())
        except Exception as e:
            st.error(f"Error loading custom outfits: {str(e)}")
            return []

CATEGORIES = [
    "Shirt", "T-shirt", "Jeans", "Jacket", "Sneakers", "Dress", "Tops",
    "Bottoms", "Outerwear", "Shoes", "Accessories", "Activewear", "Swimwear", "Sleepwear"
]

def display_outfit_item_thumbnail(item, size=150):  # Increased from 120 to 150
    try:
        if item.get("image") and os.path.exists(item["image"]):
            img = Image.open(item["image"])
            return img.resize((size, size), Image.Resampling.LANCZOS)
        return Image.new('RGB', (size, size), color=(245, 241, 236))
    except Exception:
        return Image.new('RGB', (size, size), color=(245, 241, 236))

def outfit_creation_interface(username: str):
    wardrobe_items = outfit_mgmt_db.get_user_wardrobe_for_selection(username)
    if not wardrobe_items:
        st.warning("📭 Add items to your wardrobe first to create outfits!")
        return

    # Initialize selected items in session state
    if 'selected_items' not in st.session_state:
        st.session_state.selected_items = set()

    # Item selection interface OUTSIDE the form
    st.markdown("### 🛒 Select Items for Your Outfit")
    items_by_category = {}
    for item in wardrobe_items:
        category = item.get('category', 'Other')
        items_by_category.setdefault(category, []).append(item)
    
    for category in CATEGORIES:
        if category in items_by_category:
            st.markdown(f"**{category}**")
            cols = st.columns(min(len(items_by_category[category]), 5))
            for idx, item in enumerate(items_by_category[category]):
                with cols[idx % 5]:
                    item_id = item.get('item_id')
                    if not item_id:
                        continue
                    is_selected = item_id in st.session_state.selected_items
                    thumbnail = display_outfit_item_thumbnail(item)
                    item_name = item.get('name', 'Unknown Item')
                    display_name = f"{item_name[:15]}..." if len(item_name) > 15 else item_name
                    
                    # Selection button
                    if st.button(
                        display_name,
                        key=f"select_{item_id}",
                        help=f"Click to {'remove' if is_selected else 'add'} {item_name}"
                    ):
                        if is_selected:
                            st.session_state.selected_items.discard(item_id)
                        else:
                            st.session_state.selected_items.add(item_id)
                        st.rerun()
                    
                    if is_selected:
                        st.success("✓ Selected")
                    st.image(thumbnail, width=150)  # Increased from 120 to 150

    # Display selected items count
    selected_count = len(st.session_state.selected_items)
    if selected_count > 0:
        st.info(f"✅ {selected_count} item(s) selected for this outfit")
    else:
        st.warning("⚠️ Please select at least one item for your outfit")

    # Form for outfit details
    with st.form("outfit_form", clear_on_submit=True):
        st.markdown("### 📝 Outfit Details")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Outfit Name *", placeholder="e.g., Casual Friday Look")
            description = st.text_area("Description", placeholder="Brief description of the outfit...")
            occasion = st.text_input("Occasion", placeholder="e.g., Work, Party, Date")
            season = st.text_input("Season", placeholder="e.g., Summer, Winter")
            
        with col2:
            weather_condition = st.text_input("Weather Condition", placeholder="e.g., Sunny, Rainy")
            event_type = st.text_input("Event Type", placeholder="e.g., Formal, Casual")
            day_of_week = st.text_input("Day of Week", placeholder="e.g., Monday, Weekend")
            compatibility_score = st.number_input("Compatibility Score", min_value=0, max_value=100, value=70)
            
        col3, col4 = st.columns(2)
        with col3:
            date_created = st.date_input("Date Created", value=datetime.today())
        with col4:
            last_worn = st.date_input("Last Worn", value=datetime.today())

        # Submit button
        submitted = st.form_submit_button("🎨 Create Outfit", use_container_width=True)
        
        if submitted:
            if not name.strip():
                st.error("Please enter an outfit name.")
                return
            
            if not st.session_state.selected_items:
                st.error("Please select at least one item for your outfit.")
                return
                
            success = outfit_mgmt_db.create_custom_outfit(
                username, name.strip(), description.strip(),
                weather_condition.strip(), event_type.strip(), day_of_week.strip(),
                str(date_created), str(last_worn),
                int(compatibility_score), occasion.strip(), season.strip(),
                list(st.session_state.selected_items)
            )
            if success:
                st.success("🎉 Custom outfit created successfully!")
                st.session_state.selected_items = set()  # Clear selections
                st.rerun()
            else:
                st.error("Failed to create outfit. Please try again.")

def display_custom_outfits(username: str):
    custom_outfits = outfit_mgmt_db.get_user_custom_outfits(username)
    if not custom_outfits:
        st.info("🎨 No custom outfits yet. Create your first one above!")
        return
    
    st.markdown("---")
    st.markdown("## 🧷 Your Custom Outfits")
    
    for outfit in custom_outfits:
        st.markdown("---")
        
        # Outfit header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {outfit.get('name', 'Unnamed Outfit')}")
        with col2:
            st.markdown(f"**Score: {outfit.get('compatibility_score', 0)}/100**")
        
        # Outfit details
        if outfit.get('description'):
            st.markdown(f"**Description:** {outfit.get('description')}")
        
        # Outfit metadata in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            if outfit.get('weather_condition'):
                st.markdown(f"🌤️ **Weather:** {outfit.get('weather_condition')}")
            if outfit.get('occasion'):
                st.markdown(f"🎯 **Occasion:** {outfit.get('occasion')}")
        with col2:
            if outfit.get('event_type'):
                st.markdown(f"🎪 **Event:** {outfit.get('event_type')}")
            if outfit.get('season'):
                st.markdown(f"🍂 **Season:** {outfit.get('season')}")
        with col3:
            if outfit.get('day_of_week'):
                st.markdown(f"📅 **Day:** {outfit.get('day_of_week')}")
            if outfit.get('last_worn'):
                st.markdown(f"👔 **Last Worn:** {outfit.get('last_worn')}")
        
        # Creation/update info
        if outfit.get('created_at'):
            st.caption(f"Created: {outfit.get('created_at')} | Updated: {outfit.get('updated_at', 'Never')}")
        
        # Outfit items
        items = outfit.get('items', [])
        if items:
            st.markdown("**Items in this outfit:**")
            cols = st.columns(min(len(items), 5))
            for idx, item in enumerate(items):
                with cols[idx % 5]:
                    image_path = item.get("image", "")
                    if image_path and os.path.exists(image_path):
                        img = Image.open(image_path)
                        st.image(img, width=150)  # Increased from 120 to 150
                    else:
                        st.markdown(
                            "<div style='width:150px; height:150px; background:#f0f0f0; "  # Increased from 120px to 150px
                            "display:flex; align-items:center; justify-content:center; "
                            "border-radius:8px;'>📷</div>", 
                            unsafe_allow_html=True
                        )
                    st.caption(f"**{item.get('name')}**")
                    st.caption(f"{item.get('category')} • {item.get('subcategory')}")

def outfits_page(db):
    """Main outfits page function"""
    global outfit_mgmt_db
    outfit_mgmt_db = OutfitManagementDatabase(db)
    username = st.session_state.username
    
    st.markdown("---")
    st.markdown("""
        <h1 style='font-size:2.55rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🧷 Custom Outfits
        </h1>
    """, unsafe_allow_html=True)
    
    outfit_creation_interface(username)
    display_custom_outfits(username)

if __name__ == "__main__":
    from config.database import get_database
    db = get_database()
    outfits_page(db)
