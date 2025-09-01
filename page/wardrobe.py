# import streamlit as st
# import os
# from PIL import Image
# from datetime import datetime
# from io import BytesIO
# import base64

# # V2 Database operations for wardrobe
# class WardrobeDatabase:
#     """Database operations for wardrobe management in V2"""
    
#     def __init__(self, db):
#         self.db = db
    
#     def get_category_id(self, category_name: str) -> int:
#         """Get category_id from category name"""
#         category_mapping = {
#             "Shirt": 1, "T-shirt": 2, "Jeans": 3, "Jacket": 4, "Sneakers": 5,
#             "Dress": 6, "Tops": 7, "Bottoms": 8, "Outerwear": 10, "Shoes": 11,
#             "Accessories": 12, "Activewear": 13, "Swimwear": 14, "Sleepwear": 15
#         }
#         return category_mapping.get(category_name, 1)
    
#     def get_user_wardrobe(self, username: str) -> list:
#         """Get user's wardrobe items from database"""
#         try:
#             query = """
#                 SELECT wi.*, u.username 
#                 FROM wardrobe_items wi 
#                 JOIN users u ON wi.user_id = u.user_id 
#                 WHERE u.username = %s 
#                 ORDER BY wi.created_at DESC
#             """
#             items = self.db.fetch_all(query, (username,))
            
#             # Convert database format to your existing item format
#             formatted_items = []
#             for item in items:
#                 formatted_item = {
#                     'item_id': item['id'],
#                     'name': item['name'],
#                     'category': item['category'],
#                     'subcategory': item.get('subcategory', ''),
#                     'weather_tags': item.get('weather_tags', '').split(',') if item.get('weather_tags') else [],
#                     'style_tags': item.get('style_tags', '').split(',') if item.get('style_tags') else [],
#                     'image': item.get('image_path', ''),
#                     'added_at': item['created_at'].isoformat() if item.get('created_at') else datetime.now().isoformat()
#                 }
#                 formatted_items.append(formatted_item)
#             return formatted_items
#         except Exception as e:
#             st.error(f"Error loading wardrobe: {e}")
#             return []
    
#     def add_wardrobe_item(self, username: str, item_data: dict) -> bool:
#         """Add new wardrobe item to database"""
#         try:
#             # Get user_id from username
#             user_result = self.db.fetch_one("SELECT user_id FROM users WHERE username = %s", (username,))
#             if not user_result:
#                 st.error("User not found")
#                 return False
            
#             user_id = user_result['user_id']
#             category_id = self.get_category_id(item_data['category'])
            
#             # FIXED: Store subcategory as text, set subcategory_id to NULL (or a default value)
#             query = """
#                 INSERT INTO wardrobe_items 
#                 (user_id, name, category, category_id, subcategory, subcategory_id, color, brand, size, 
#                  image_path, weather_tags, style_tags)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
            
#             weather_tags_str = ','.join(item_data.get('weather_tags', []))
#             style_tags_str = ','.join(item_data.get('style_tags', []))
            
#             result = self.db.insert_data(query, (
#                 user_id,
#                 item_data['name'],
#                 item_data['category'],
#                 category_id,
#                 item_data.get('subcategory', ''),  # Store as text in subcategory column
#                 None,  # Set subcategory_id to NULL since we don't have a subcategory mapping table
#                 item_data.get('color', ''),
#                 item_data.get('brand', ''),
#                 item_data.get('size', ''),
#                 item_data.get('image', ''),
#                 weather_tags_str,
#                 style_tags_str
#             ))
            
#             return result is not None
#         except Exception as e:
#             st.error(f"Error adding item: {e}")
#             return False
    
#     def update_wardrobe_item(self, username: str, item_id: int, item_data: dict) -> bool:
#         """Update existing wardrobe item in database"""
#         try:
#             # Verify item belongs to user
#             verify_result = self.db.fetch_one("""
#                 SELECT wi.id FROM wardrobe_items wi 
#                 JOIN users u ON wi.user_id = u.user_id 
#                 WHERE wi.id = %s AND u.username = %s
#             """, (item_id, username))
            
#             if not verify_result:
#                 st.error("Item not found or access denied")
#                 return False
            
#             category_id = self.get_category_id(item_data['category'])
            
#             # FIXED: Update subcategory as text, set subcategory_id to NULL
#             query = """
#                 UPDATE wardrobe_items SET 
#                 name = %s, category = %s, category_id = %s, subcategory = %s, subcategory_id = %s,
#                 image_path = %s, weather_tags = %s, style_tags = %s,
#                 updated_at = NOW()
#                 WHERE id = %s
#             """
            
#             weather_tags_str = ','.join(item_data.get('weather_tags', []))
#             style_tags_str = ','.join(item_data.get('style_tags', []))
            
#             result = self.db.update_data(query, (
#                 item_data['name'],
#                 item_data['category'],
#                 category_id,
#                 item_data.get('subcategory', ''),  # Store as text in subcategory column
#                 None,  # Set subcategory_id to NULL
#                 item_data.get('image', ''),
#                 weather_tags_str,
#                 style_tags_str,
#                 item_id
#             ))
            
#             return result > 0
#         except Exception as e:
#             st.error(f"Error updating item: {e}")
#             return False
    
#     def delete_wardrobe_item(self, username: str, item_id: int) -> bool:
#         """Delete wardrobe item from database"""
#         try:
#             result = self.db.fetch_one("""
#                 SELECT wi.image_path FROM wardrobe_items wi 
#                 JOIN users u ON wi.user_id = u.user_id 
#                 WHERE wi.id = %s AND u.username = %s
#             """, (item_id, username))
            
#             if not result:
#                 st.error("Item not found or access denied")
#                 return False
            
#             deleted_rows = self.db.delete_data("DELETE FROM wardrobe_items WHERE id = %s", (item_id,))
            
#             # Clean up image file if exists
#             if result.get('image_path') and os.path.exists(result['image_path']):
#                 try:
#                     os.remove(result['image_path'])
#                 except OSError:
#                     pass  # File cleanup is non-critical
            
#             return deleted_rows > 0
#         except Exception as e:
#             st.error(f"Error deleting item: {e}")
#             return False
    
#     def get_wardrobe_item_by_id(self, username: str, item_id: int) -> dict:
#         """Get specific wardrobe item by ID"""
#         try:
#             query = """
#                 SELECT wi.*, u.username 
#                 FROM wardrobe_items wi 
#                 JOIN users u ON wi.user_id = u.user_id 
#                 WHERE wi.id = %s AND u.username = %s
#             """
#             item = self.db.fetch_one(query, (item_id, username))
            
#             if not item:
#                 return None
            
#             return {
#                 'item_id': item['id'],
#                 'name': item['name'],
#                 'category': item['category'],
#                 'subcategory': item.get('subcategory', ''),
#                 'weather_tags': item.get('weather_tags', '').split(',') if item.get('weather_tags') else [],
#                 'style_tags': item.get('style_tags', '').split(',') if item.get('style_tags') else [],
#                 'image': item.get('image_path', ''),
#                 'added_at': item['created_at'].isoformat() if item.get('created_at') else datetime.now().isoformat()
#             }
#         except Exception as e:
#             st.error(f"Error loading item: {e}")
#             return None


# # Complete categories structure based on your SQL data
# CATEGORIES = {
#     "Shirt": [
#         "Formal Shirts", "Casual Shirts", "Dress Shirts", "Button-up Shirts", 
#         "Flannel Shirts", "Polo Shirts"
#     ],
#     "T-shirt": [
#         "Basic Tees", "Graphic Tees", "V-Neck Tees", "Crew Neck Tees", "Long Sleeve Tees"
#     ],
#     "Jeans": [
#         "Skinny Jeans", "Straight Fit", "Wide-Legged", "Bell Bottoms", 
#         "Bootcut Jeans", "Ripped Jeans"
#     ],
#     "Jacket": [
#         "Leather Jackets", "Denim Jackets", "Bomber Jackets", "Windbreakers"
#     ],
#     "Sneakers": [
#         "Running Shoes", "High-tops", "Low-tops", "Basketball Shoes", "Casual Sneakers"
#     ],
#     "Dress": [
#         "Maxi", "Midi", "Mini", "Bodycon", "Shirt Dress", "Wrap Dress", "A-Line", 
#         "Fit & Flare", "Slip Dress", "Cocktail Dress", "Evening Gown", "Casual Dress", 
#         "Beach Dress", "Party Dress", "Formal Dresses", "Sundresses"
#     ],
#     "Tops": [
#         "Crop Tops", "Tank Tops", "Blouses", "Hoodies", "Sweaters", "Cardigans", 
#         "Blazers", "Cut Sleeves", "Full Sleeves"
#     ],
#     "Bottoms": [
#         "Shorts", "Skirts", "Palazzos", "Trousers", "Track Pants", "Leggings", 
#         "Culottes", "Capris", "Cargo Pants", "Joggers", "Chinos"
#     ],
#     "Outerwear": [
#         "Coats", "Trench Coats", "Puffer Jackets", "Peacoats", "Parkas"
#     ],
#     "Shoes": [
#         "Heels", "Flats", "Boots", "Sandals", "Pumps", "Wedges", "Loafers", 
#         "Oxford", "Ballet Flats", "Ankle Boots", "Knee-High Boots", "Flip Flops", 
#         "Espadrilles", "Platform Shoes"
#     ],
#     "Accessories": [
#         "Bags", "Belts", "Scarves", "Jewelry", "Sunglasses", "Handbags", 
#         "Clutches", "Backpacks", "Watches", "Hats", "Hair Accessories", 
#         "Necklaces", "Earrings", "Bracelets", "Rings"
#     ],
#     "Activewear": [
#         "Sports Bras", "Yoga Pants", "Athletic Shorts", "Workout Tanks"
#     ],
#     "Swimwear": [
#         "Bikinis", "One-pieces", "Swim Shorts", "Cover-ups"
#     ],
#     "Sleepwear": [
#         "Pajamas", "Nightgowns", "Robes", "Sleep Shorts"
#     ]
# }

# # Final optimized weather tags (overlaps removed, air conditioned removed)
# WEATHER_TAGS = [
#     "Hot", "Cold", "Freezing", "Mild", 
#     "Rainy", "Windy", "Sunny", "Cloudy", "Snowy", "Stormy",
#     "Humid", "Dry"
# ]

# # UPDATED: Two separate tag systems
# # Occasion/Activity Tags (when/where to wear)
# OCCASION_STYLE_TAGS = {
#     "Core Dress Codes": ["Casual", "Formal", "Comfortable"],
#     "Social Events": ["Party", "Date", "Wedding", "Cocktail"],
#     "Daily Activities": ["Work", "Shopping", "Brunch", "Dinner", "Meeting", "Interview"],
#     "Fitness & Sports": ["Sport", "Gym", "Yoga"],
#     "Leisure": ["Beach", "Vacation", "Lounging", "Home"],
#     "Entertainment": ["Festival", "Concert", "Theater", "Picnic"],
#     "Celebrations": ["Birthday", "Graduation"]
# }

# # Mood/Aesthetic Tags (style/feeling of clothing)
# MOOD_STYLE_TAGS = [
#     "Streetwear", "Boho", "Vintage", "Classic", "Trendy", "Minimalist", 
#     "Elegant", "Chic", "Edgy", "Romantic", "Preppy", "Sporty Chic", "Confident"
# ]

# def get_all_occasion_tags():
#     """Helper function to get all occasion tags as a flat list"""
#     all_tags = []
#     for category_tags in OCCASION_STYLE_TAGS.values():
#         all_tags.extend(category_tags)
#     return all_tags

# def get_all_style_tags():
#     """Helper function to get all style tags (both occasion and mood) as a flat list"""
#     all_tags = []
#     # Add occasion tags
#     for category_tags in OCCASION_STYLE_TAGS.values():
#         all_tags.extend(category_tags)
#     # Add mood tags
#     all_tags.extend(MOOD_STYLE_TAGS)
#     return all_tags

# def get_category_icon(category: str) -> str:
#     """Get emoji icon for category"""
#     category_icons = {
#         'Shirt': "👔", 'T-shirt': "👕", 'Jeans': "👖", 'Jacket': "🧥", 
#         'Sneakers': "👟", 'Dress': "👗", 'Tops': "👚", 'Bottoms': "👖",
#         'Outerwear': "🧥", 'Shoes': "👠", 'Accessories': "👜", 
#         'Activewear': "🏃‍♀️", 'Swimwear': "👙", 'Sleepwear': "👘"
#     }
#     return category_icons.get(category, "🧺")

# IMAGE_FOLDER = os.path.join("assets", "images")

# st.markdown("""
# <style>
#     /* Hide the problematic sidebar collapse button */
#     .stSidebar > div > div > button {
#         display: none !important;
#     }
    
#     /* Hide keyboard_left_arrow text in sidebar */
#     .stSidebar [data-testid="stMarkdownContainer"] p:contains("keyboard_arrow_left"),
#     .stSidebar [data-testid="stMarkdownContainer"]:has-text("keyboard_arrow_left") {
#         display: none !important;
#     }
    
#     /* More comprehensive hiding of the arrow text */
#     .stSidebar *:contains("keyboard_arrow_left") {
#         display: none !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Ensure directory exists
# if not os.path.exists(IMAGE_FOLDER):
#     os.makedirs(IMAGE_FOLDER, exist_ok=True)

# # ----------- CUSTOM GLOBAL STYLES -----------
# st.markdown("""
# <style>
#     .subheading {
#         font-size: 1.4rem !important;
#         font-weight: 700 !important;
#         color: #4a2511;
#         margin-bottom: 0.25em;
#     }
#     .wardrobe-form-card {
#         background: #fefcfa;
#         border-radius: 12px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         border: 1px solid #e8ddd4;
#     }
#     /* Sidebar background gradient */
#     section[data-testid="stSidebar"] > div {
#         background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;
#     }
#     /* Style tags expander styling */
#     .style-tags-container {
#         margin-top: 10px;
#         margin-bottom: 15px;
#     }
#     /* Custom expander styling for better appearance */
#     .streamlit-expanderHeader {
#         background-color: #f8f4f0 !important;
#         border-radius: 8px !important;
#         border: 1px solid #e8ddd4 !important;
#         margin-bottom: 5px !important;
#     }
#     /* Style the expander content */
#     .streamlit-expanderContent {
#         background-color: #fefcfa !important;
#         border: 1px solid #e8ddd4 !important;
#         border-top: none !important;
#         border-radius: 0 0 8px 8px !important;
#         padding: 10px !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# def wardrobe_page(db):
#     """Wardrobe page with database parameter"""
#     # Initialize database service with database connection
#     global wardrobe_db
#     wardrobe_db = WardrobeDatabase(db)
    
#     username = st.session_state.username
#     st.markdown("---")
#     st.markdown("""
#         <h1 style='font-size:2.25rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
#         🧥 Your Wardrobe
#         </h1>
#     """, unsafe_allow_html=True)
#     add_enhanced_item_form(username)
#     show_wardrobe_management(username)

# # V2 Wrapper functions to maintain compatibility
# def get_user_wardrobe(username: str) -> list:
#     return wardrobe_db.get_user_wardrobe(username)

# def add_wardrobe_item(username: str, item_data: dict) -> bool:
#     return wardrobe_db.add_wardrobe_item(username, item_data)

# def update_wardrobe_item(username: str, item_id: int, item_data: dict) -> bool:
#     return wardrobe_db.update_wardrobe_item(username, item_id, item_data)

# def delete_wardrobe_item(username: str, item_id: int) -> bool:
#     return wardrobe_db.delete_wardrobe_item(username, item_id)

# def get_wardrobe_item_by_id(username: str, item_id: int) -> dict:
#     return wardrobe_db.get_wardrobe_item_by_id(username, item_id)

# def show_wardrobe_management(username):
#     items = get_user_wardrobe(username)
    
#     with st.sidebar:
#         st.markdown("""<style>.css-1d391kg {
#         background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;}
#         section[data-testid="stSidebar"] > div {
#         background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;}
#         </style>""", unsafe_allow_html=True)

#         st.markdown("""<h1 style='font-size:1.35rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
#         🔍 Search & Filters</h1>""", unsafe_allow_html=True)
#         search_query = st.text_input("Search items...", placeholder="e.g., blue shirt")
    
#         st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
#         🏷️ Filters</h1>""", unsafe_allow_html=True)
#         weather_filter = st.multiselect("Weather Tags", WEATHER_TAGS, key="weather_filter")
        
#         # NEW: Separate filters for occasion and mood tags
#         occasion_filter = st.multiselect("📅 Occasion Tags", get_all_occasion_tags(), key="occasion_filter")
#         mood_filter = st.multiselect("🎧 Mood Tags", MOOD_STYLE_TAGS, key="mood_filter")
    
#         st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
#         📂 Category Filter </h1>""", unsafe_allow_html=True) 
#         selected_category = st.session_state.get('active_category', 'All')
    
#         col_cat_all, = st.columns([1])
#         if col_cat_all.button("All Items", key="cat_all_sidebar", use_container_width=True):
#             st.session_state['active_category'] = 'All'
#             st.rerun()
        
#         for category in CATEGORIES.keys():
#             if st.button(f"{get_category_icon(category)} {category}", key=f"cat_{category}_sidebar", use_container_width=True):
#                 st.session_state['active_category'] = category
#                 st.rerun()

#     # Apply filters
#     filtered_items = items.copy()
    
#     # Search filter
#     if search_query:
#         filtered_items = [
#             item for item in filtered_items
#             if search_query.lower() in item.get("name", "").lower()
#             or search_query.lower() in item.get("category", "").lower()
#             or search_query.lower() in item.get("subcategory", "").lower()
#         ]
    
#     # Category filter
#     selected_category = st.session_state.get('active_category', 'All')
#     if selected_category != "All":
#         filtered_items = [item for item in filtered_items if item.get("category") == selected_category]
    
#     # Weather filter
#     if weather_filter:
#         filtered_items = [
#             item for item in filtered_items
#             if any(tag in item.get("weather_tags", []) for tag in weather_filter)
#         ]
    
#     # NEW: Occasion filter
#     if occasion_filter:
#         filtered_items = [
#             item for item in filtered_items
#             if any(tag in item.get("style_tags", []) for tag in occasion_filter)
#         ]
    
#     # NEW: Mood filter
#     if mood_filter:
#         filtered_items = [
#             item for item in filtered_items
#             if any(tag in item.get("style_tags", []) for tag in mood_filter)
#         ]
    
#     # Display items
#     st.markdown("---")
#     st.markdown("### 👔 Your Wardrobe Collection")
    
#     if not filtered_items:
#         st.info("📭 No items found. Try adjusting your filters or add some items!")
#     else:
#         cols_per_row = 3
#         for i in range(0, len(filtered_items), cols_per_row):
#             cols = st.columns(cols_per_row)
#             for j in range(cols_per_row):
#                 if i + j < len(filtered_items):
#                     item = filtered_items[i + j]
#                     with cols[j]:
#                         show_item_card(username, item)
    
#     st.markdown("---")

# def show_item_card(username, item):
#     # Get category icon
#     category_icon = get_category_icon(item.get("category", ""))

#     # Prepare badges with improved display for two tag types
#     if item.get("weather_tags"):
#         weather_badge = (
#             "<span style='color:#313131; padding:3px 10px;"
#             "border-radius:12px; font-size:0.85rem; font-weight:600; margin-right:0.4em;'>"
#             f"🌤️ {', '.join([t.title() for t in item['weather_tags']])}"
#             "</span>"
#         )
#     else:
#         weather_badge = ""
    
#     # Separate occasion and mood tags for display on different lines
#     occasion_tags = []
#     mood_tags = []
    
#     for tag in item.get("style_tags", []):
#         if tag in get_all_occasion_tags():
#             occasion_tags.append(tag)
#         elif tag in MOOD_STYLE_TAGS:
#             mood_tags.append(tag)
    
#     # Create separate badge lines for occasion and mood tags
#     occasion_badge = ""
#     mood_badge = ""
    
#     if occasion_tags:
#         occasion_badge = (
#             "<span style='color:#444; padding:3px 10px;"
#             "border-radius:12px; font-size:0.85rem; font-weight:600; margin-right:0.4em;'>"
#             f"📅 {', '.join([t.title() for t in occasion_tags])}"
#             "</span>"
#         )
    
#     if mood_tags:
#         mood_badge = (
#             "<span style='color:#444; padding:3px 10px;"
#             "border-radius:12px; font-size:0.85rem; font-weight:600;'>"
#             f"🎧 {', '.join([t.title() for t in mood_tags])}"
#             "</span>"
#         )

#     # Image block: fixed, square, centered
#     image_html = ""
#     if item.get("image") and os.path.exists(item["image"]):
#         try:
#             img = Image.open(item["image"])
#             min_dim = min(img.size)
#             left = (img.width - min_dim) // 2
#             top = (img.height - min_dim) // 2
#             right = left + min_dim
#             bottom = top + min_dim
#             img_cropped = img.crop((left, top, right, bottom))
#             img_cropped = img_cropped.resize((200, 200), Image.LANCZOS)
#             buffered = BytesIO()
#             img_cropped.save(buffered, format="PNG", quality=95)
#             img_str = base64.b64encode(buffered.getvalue()).decode()
#             image_html = f"<img src='data:image/png;base64,{img_str}' style='width:200px; height:200px; object-fit:cover; display:block; margin:auto;'/>"
#         except (FileNotFoundError, OSError, IOError) as e:
#             st.warning(f"Could not load image: {str(e)}")
#             image_html = "<div style='height:200px; width:200px; background:#f2f2f2; color:#888; display:flex; align-items:center; justify-content:center;'>📷</div>"
#     else:
#         image_html = "<div style='height:200px; width:200px; background:#f2f2f2; color:#888; display:flex; align-items:center; justify-content:center;'>📷</div>"

#     # Create a container div that wraps both the card and buttons to ensure proper alignment
#     st.markdown(f"""
#         <div style='width: 100%; display: flex; flex-direction: column; align-items: center; margin-bottom: 1.5em;'>
#             <div style='
#                 background: #fcf7ed;
#                 border-radius: 18px;
#                 box-shadow: 0 4px 15px #d4b29e20;
#                 margin-bottom: 0.8em;
#                 margin-top: 0.2em;
#                 padding: 1.1em 1em 0.95em 1.2em;
#                 width: 100%;
#                 max-width: 280px;
#                 min-height: 400px;
#                 box-sizing: border-box;
#                 overflow: auto;
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 justify-content: flex-start;
#                 position: relative;
#             '>
#                 {image_html}
#                 <div style='font-size:1.23rem; font-weight:800; color:#4a2511;
#                              margin-bottom:3px; margin-top:5px;
#                              overflow-wrap: break-word; max-width: 240px; text-align: center;'>
#                     {category_icon} {item.get("name", "Unnamed Item")}
#                 </div>
#                 <div style='color:#7a5d42; font-weight:600; margin-bottom:0.5em; font-size:1.06rem;
#                             overflow-wrap: break-word; max-width: 240px; text-align: center;'>
#                     {item.get("category", "")} &bull; {item.get("subcategory", "")}
#                 </div>
#                 <div style='margin-bottom:4px; max-width:240px; text-align:left; overflow-wrap:break-word;
#                             white-space: normal; line-height: 1.4;'>
#                     <div style='margin-bottom: 5px;'>{weather_badge}</div>
#                     <div style='margin-bottom: 3px;'>{occasion_badge}</div>
#                     <div>{mood_badge}</div>
#                 </div>
#                 <div style='flex:1;'></div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

#     # Action buttons below the card - now properly aligned with the card width
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("✏️ Edit", key=f"edit_{item.get('item_id')}", use_container_width=True, help="Edit item details"):
#             st.session_state.editing_item = item.get('item_id')
#             st.rerun()
#     with col2:
#         if st.button("🗑️ Delete", key=f"delete_{item.get('item_id')}", use_container_width=True, help="Delete this item"):
#             if delete_wardrobe_item(username, item.get('item_id')):
#                 st.success("Item deleted successfully!")
#                 st.rerun()
#             else:
#                 st.error("Failed to delete item.")

# def add_enhanced_item_form(username):
#     editing_item_id = st.session_state.get("editing_item")
#     editing_item = None
#     if editing_item_id:
#         editing_item = get_wardrobe_item_by_id(username, editing_item_id)
#         if editing_item is None:
#             st.session_state.editing_item = None
#             st.rerun()

#     st.markdown("""
#         <h1 style='font-size:1.5rem; font-weight:500; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
#         📂 Add or Edit an Item
#         </h1>
#     """, unsafe_allow_html=True)
    
#     st.markdown('<div class="wardrobe-form-card">', unsafe_allow_html=True)
    
#     col_cat1, col_cat2 = st.columns(2)
#     with col_cat1:
#         st.markdown('<span style="font-weight:700">Category *</span>', unsafe_allow_html=True)
#         selected_category = st.selectbox(
#             "",
#             list(CATEGORIES.keys()),
#             index=list(CATEGORIES.keys()).index(editing_item.get('category', 'Shirt'))
#             if editing_item and editing_item.get('category') in CATEGORIES else 0,
#             key="category_selector",
#             label_visibility='collapsed'
#         )
    
#     with col_cat2:
#         st.markdown('<span style="font-weight:700">Subcategory *</span>', unsafe_allow_html=True)
#         available_subcategories = CATEGORIES[selected_category]
#         selected_subcategory = st.selectbox(
#             "",
#             available_subcategories,
#             index=available_subcategories.index(
#                 editing_item.get('subcategory', available_subcategories[0])
#             )
#             if editing_item and editing_item.get('subcategory') in available_subcategories else 0,
#             key="subcategory_selector",
#             label_visibility='collapsed'
#         )
    
#     # Use unique form keys to prevent conflicts
#     form_key = f"edit_item_form_{username}_{editing_item_id}" if editing_item else f"add_item_form_{username}"
    
#     with st.form(form_key, clear_on_submit=not bool(editing_item)):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown('<span style="font-weight:700">📋 Item Name *</span>', unsafe_allow_html=True)
#             name = st.text_input(
#                 "",
#                 value=editing_item.get('name', '') if editing_item else '',
#                 placeholder="e.g., Blue Cotton T-Shirt",
#                 label_visibility='collapsed'
#             )
            
#             st.info(f"📂**Category:** {selected_category} • {selected_subcategory}")
            
#             # File upload section - moved up and aligned with style tags in column 2
#             st.markdown('<span style="font-weight:700">📷 Upload Image *</span>', unsafe_allow_html=True)
#             if not editing_item:
#                 st.caption("📷 Maximum file size: 200MB. Supported formats: JPG, JPEG, PNG")
#                 image_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility='collapsed')
#             else:
#                 st.markdown('<span style="font-weight:700">Current Image:</span>', unsafe_allow_html=True)
#                 if editing_item.get("image") and os.path.exists(editing_item["image"]):
#                     try:
#                         img = Image.open(editing_item["image"])
#                         st.image(img, width=170)
#                     except Exception as e:
#                         st.write(f"Image unavailable: {str(e)}")
#                 st.caption("📷 Maximum file size: 200MB. Supported formats: JPG, JPEG, PNG")
#                 image_file = st.file_uploader("Replace Image (optional)", type=["jpg", "jpeg", "png"])
        
#         with col2:
#             st.markdown('<span style="font-weight:700">🌤️ Weather Suitability</span>', unsafe_allow_html=True)
#             st.caption("Select weather conditions where this item is appropriate")
#             st.markdown('<span> Weather Tags *</span>', unsafe_allow_html=True)
#             weather_tags = st.multiselect(
#                 "",
#                 WEATHER_TAGS,
#                 default=editing_item.get('weather_tags', []) if editing_item else [],
#                 help="Choose weather conditions this item is suitable for",
#                 label_visibility='collapsed'
#             )
            
#             # NEW: Two-category style tag system
#             st.markdown('<span style="font-weight:700">👗 Style & Occasion</span>', unsafe_allow_html=True)
#             st.caption("Select occasions and mood/aesthetic for this item")
            
#             # Get current tags for editing
#             current_occasion_tags = []
#             current_mood_tags = []
#             if editing_item and editing_item.get('style_tags'):
#                 for tag in editing_item.get('style_tags', []):
#                     if tag in get_all_occasion_tags():
#                         current_occasion_tags.append(tag)
#                     elif tag in MOOD_STYLE_TAGS:
#                         current_mood_tags.append(tag)
            
#             # Occasion tags selection
#             st.markdown('<span>📅 Occasion Tags *</span>', unsafe_allow_html=True)
#             occasion_tags = st.multiselect(
#                 "",
#                 get_all_occasion_tags(),
#                 default=current_occasion_tags,
#                 help="Choose occasions and activities for this item",
#                 label_visibility='collapsed',
#                 key="occasion_multiselect"
#             )
            
#             # Mood/Aesthetic tags selection
#             st.markdown('<span>🎧 Mood/Aesthetic Tags *</span>', unsafe_allow_html=True)
#             mood_tags = st.multiselect(
#                 "",
#                 MOOD_STYLE_TAGS,
#                 default=current_mood_tags,
#                 help="Choose the mood or aesthetic style of this item",
#                 label_visibility='collapsed',
#                 key="mood_multiselect"
#             )
            
#             # Combine both tag types for final style_tags
#             style_tags = occasion_tags + mood_tags
        
#         st.info("💡 **Tip:** Select both occasion and mood tags to make your outfit recommendations more accurate!")
        
#         # Form buttons
#         if editing_item:
#             col_spacer1, col_submit, col_cancel, col_spacer2 = st.columns([1, 1, 1, 1])
#             with col_submit:
#                 submitted = st.form_submit_button("💾 Update Item", use_container_width=True)
#             with col_cancel:
#                 if st.form_submit_button("❌ Cancel Edit", use_container_width=True):
#                     st.session_state.editing_item = None
#                     st.rerun()
#         else:
#             col_spacer1, col_submit, col_spacer2 = st.columns([1, 2, 1])
#             with col_submit:
#                 submitted = st.form_submit_button("╰┈➤🚪 Add to Wardrobe", use_container_width=True)
        
#         # Form submission handling
#         if submitted:
#             if not name.strip():
#                 st.error("Please enter an item name.")
#             elif not weather_tags:
#                 st.error("Please select at least one weather tag.")
#             elif not occasion_tags and not mood_tags:
#                 st.error("Please select at least one occasion tag or mood tag.")
#             elif not editing_item and not image_file:
#                 st.error("Please upload an image.")
#             else:
#                 try:
#                     image_path = None
#                     if image_file is not None:
#                         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                         filename = f"{timestamp}_{username}_{image_file.name}"
#                         image_path = os.path.join(IMAGE_FOLDER, filename)
#                         with open(image_path, "wb") as f:
#                             f.write(image_file.getbuffer())
#                     elif editing_item:
#                         image_path = editing_item.get("image", "")
                    
#                     item_data = {
#                         "name": name.strip(),
#                         "category": selected_category,
#                         "subcategory": selected_subcategory,
#                         "weather_tags": weather_tags,
#                         "style_tags": style_tags,  # This now contains both occasion and mood tags
#                         "image": image_path,
#                         "added_at": editing_item.get("added_at", datetime.now().isoformat()) if editing_item else datetime.now().isoformat()
#                     }
                    
#                     if editing_item:
#                         if update_wardrobe_item(username, editing_item_id, item_data):
#                             st.success("🎉 Item updated successfully!")
#                             st.session_state.editing_item = None
#                             st.rerun()
#                         else:
#                             st.error("Failed to update item.")
#                     else:
#                         if add_wardrobe_item(username, item_data):
#                             st.success("🎉 Item added successfully!")
#                             st.rerun()
#                         else:
#                             st.error("Failed to add item.")
                            
#                 except Exception as e:
#                     st.error(f"Error processing item: {str(e)}")
    
#     st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import os
from PIL import Image
from datetime import datetime
from io import BytesIO
import base64


# V2 Database operations for wardrobe
class WardrobeDatabase:
    """Database operations for wardrobe management in V2"""
    
    def __init__(self, db):
        self.db = db
    
    def get_category_id(self, category_name: str) -> int:
        """Get category_id from category name"""
        category_mapping = {
            "Shirt": 1, "T-shirt": 2, "Jeans": 3, "Jacket": 4, "Sneakers": 5,
            "Dress": 6, "Tops": 7, "Bottoms": 8, "Outerwear": 10, "Shoes": 11,
            "Accessories": 12, "Activewear": 13, "Swimwear": 14, "Sleepwear": 15
        }
        return category_mapping.get(category_name, 1)
    
    def get_user_wardrobe(self, username: str) -> list:
        """Get user's wardrobe items from database"""
        try:
            query = """
                SELECT wi.*, u.username 
                FROM wardrobe_items wi 
                JOIN users u ON wi.user_id = u.user_id 
                WHERE u.username = %s 
                ORDER BY wi.created_at DESC
            """
            items = self.db.fetch_all(query, (username,))
            
            # Convert database format to your existing item format
            formatted_items = []
            for item in items:
                formatted_item = {
                    'item_id': item['id'],
                    'name': item['name'],
                    'category': item['category'],
                    'subcategory': item.get('subcategory', ''),
                    'weather_tags': item.get('weather_tags', '').split(',') if item.get('weather_tags') else [],
                    'style_tags': item.get('style_tags', '').split(',') if item.get('style_tags') else [],
                    'image': item.get('image_path', ''),
                    'added_at': item['created_at'].isoformat() if item.get('created_at') else datetime.now().isoformat()
                }
                formatted_items.append(formatted_item)
            return formatted_items
        except Exception as e:
            st.error(f"Error loading wardrobe: {e}")
            return []
    
    def add_wardrobe_item(self, username: str, item_data: dict) -> bool:
        """Add new wardrobe item to database"""
        try:
            # Get user_id from username
            user_result = self.db.fetch_one("SELECT user_id FROM users WHERE username = %s", (username,))
            if not user_result:
                st.error("User not found")
                return False
            
            user_id = user_result['user_id']
            category_id = self.get_category_id(item_data['category'])
            
            # FIXED: Store subcategory as text, set subcategory_id to NULL (or a default value)
            query = """
                INSERT INTO wardrobe_items 
                (user_id, name, category, category_id, subcategory, subcategory_id, color, brand, size, 
                 image_path, weather_tags, style_tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            weather_tags_str = ','.join(item_data.get('weather_tags', []))
            style_tags_str = ','.join(item_data.get('style_tags', []))
            
            result = self.db.insert_data(query, (
                user_id,
                item_data['name'],
                item_data['category'],
                category_id,
                item_data.get('subcategory', ''),  # Store as text in subcategory column
                None,  # Set subcategory_id to NULL since we don't have a subcategory mapping table
                item_data.get('color', ''),
                item_data.get('brand', ''),
                item_data.get('size', ''),
                item_data.get('image', ''),
                weather_tags_str,
                style_tags_str
            ))
            
            return result is not None
        except Exception as e:
            st.error(f"Error adding item: {e}")
            return False
    
    def update_wardrobe_item(self, username: str, item_id: int, item_data: dict) -> bool:
        """Update existing wardrobe item in database"""
        try:
            # Verify item belongs to user
            verify_result = self.db.fetch_one("""
                SELECT wi.id FROM wardrobe_items wi 
                JOIN users u ON wi.user_id = u.user_id 
                WHERE wi.id = %s AND u.username = %s
            """, (item_id, username))
            
            if not verify_result:
                st.error("Item not found or access denied")
                return False
            
            category_id = self.get_category_id(item_data['category'])
            
            # FIXED: Update subcategory as text, set subcategory_id to NULL
            query = """
                UPDATE wardrobe_items SET 
                name = %s, category = %s, category_id = %s, subcategory = %s, subcategory_id = %s,
                image_path = %s, weather_tags = %s, style_tags = %s,
                updated_at = NOW()
                WHERE id = %s
            """
            
            weather_tags_str = ','.join(item_data.get('weather_tags', []))
            style_tags_str = ','.join(item_data.get('style_tags', []))
            
            result = self.db.update_data(query, (
                item_data['name'],
                item_data['category'],
                category_id,
                item_data.get('subcategory', ''),  # Store as text in subcategory column
                None,  # Set subcategory_id to NULL
                item_data.get('image', ''),
                weather_tags_str,
                style_tags_str,
                item_id
            ))
            
            return result > 0
        except Exception as e:
            st.error(f"Error updating item: {e}")
            return False
    
    def delete_wardrobe_item(self, username: str, item_id: int) -> bool:
        """Delete wardrobe item from database"""
        try:
            result = self.db.fetch_one("""
                SELECT wi.image_path FROM wardrobe_items wi 
                JOIN users u ON wi.user_id = u.user_id 
                WHERE wi.id = %s AND u.username = %s
            """, (item_id, username))
            
            if not result:
                st.error("Item not found or access denied")
                return False
            
            deleted_rows = self.db.delete_data("DELETE FROM wardrobe_items WHERE id = %s", (item_id,))
            
            # Clean up image file if exists
            if result.get('image_path') and os.path.exists(result['image_path']):
                try:
                    os.remove(result['image_path'])
                except OSError:
                    pass  # File cleanup is non-critical
            
            return deleted_rows > 0
        except Exception as e:
            st.error(f"Error deleting item: {e}")
            return False
    
    def get_wardrobe_item_by_id(self, username: str, item_id: int) -> dict:
        """Get specific wardrobe item by ID"""
        try:
            query = """
                SELECT wi.*, u.username 
                FROM wardrobe_items wi 
                JOIN users u ON wi.user_id = u.user_id 
                WHERE wi.id = %s AND u.username = %s
            """
            item = self.db.fetch_one(query, (item_id, username))
            
            if not item:
                return None
            
            return {
                'item_id': item['id'],
                'name': item['name'],
                'category': item['category'],
                'subcategory': item.get('subcategory', ''),
                'weather_tags': item.get('weather_tags', '').split(',') if item.get('weather_tags') else [],
                'style_tags': item.get('style_tags', '').split(',') if item.get('style_tags') else [],
                'image': item.get('image_path', ''),
                'added_at': item['created_at'].isoformat() if item.get('created_at') else datetime.now().isoformat()
            }
        except Exception as e:
            st.error(f"Error loading item: {e}")
            return None


# Complete categories structure based on your SQL data
CATEGORIES = {
    "Shirt": [
        "Formal Shirts", "Casual Shirts", "Dress Shirts", "Button-up Shirts", 
        "Flannel Shirts", "Polo Shirts"
    ],
    "T-shirt": [
        "Basic Tees", "Graphic Tees", "V-Neck Tees", "Crew Neck Tees", "Long Sleeve Tees"
    ],
    "Jeans": [
        "Skinny Jeans", "Straight Fit", "Wide-Legged", "Bell Bottoms", 
        "Bootcut Jeans", "Ripped Jeans"
    ],
    "Jacket": [
        "Leather Jackets", "Denim Jackets", "Bomber Jackets", "Windbreakers"
    ],
    "Sneakers": [
        "Running Shoes", "High-tops", "Low-tops", "Basketball Shoes", "Casual Sneakers"
    ],
    "Dress": [
        "Maxi", "Midi", "Mini", "Bodycon", "Shirt Dress", "Wrap Dress", "A-Line", 
        "Fit & Flare", "Slip Dress", "Cocktail Dress", "Evening Gown", "Casual Dress", 
        "Beach Dress", "Party Dress", "Formal Dresses", "Sundresses"
    ],
    "Tops": [
        "Crop Tops", "Tank Tops", "Blouses", "Hoodies", "Sweaters", "Cardigans", 
        "Blazers", "Cut Sleeves", "Full Sleeves"
    ],
    "Bottoms": [
        "Shorts", "Skirts", "Palazzos", "Trousers", "Track Pants", "Leggings", 
        "Culottes", "Capris", "Cargo Pants", "Joggers", "Chinos"
    ],
    "Outerwear": [
        "Coats", "Trench Coats", "Puffer Jackets", "Peacoats", "Parkas"
    ],
    "Shoes": [
        "Heels", "Flats", "Boots", "Sandals", "Pumps", "Wedges", "Loafers", 
        "Oxford", "Ballet Flats", "Ankle Boots", "Knee-High Boots", "Flip Flops", 
        "Espadrilles", "Platform Shoes"
    ],
    "Accessories": [
        "Bags", "Belts", "Scarves", "Jewelry", "Sunglasses", "Handbags", 
        "Clutches", "Backpacks", "Watches", "Hats", "Hair Accessories", 
        "Necklaces", "Earrings", "Bracelets", "Rings"
    ],
    "Activewear": [
        "Sports Bras", "Yoga Pants", "Athletic Shorts", "Workout Tanks"
    ],
    "Swimwear": [
        "Bikinis", "One-pieces", "Swim Shorts", "Cover-ups"
    ],
    "Sleepwear": [
        "Pajamas", "Nightgowns", "Robes", "Sleep Shorts"
    ]
}

# Final optimized weather tags (overlaps removed, air conditioned removed)
WEATHER_TAGS = [
    "Hot", "Cold", "Freezing", "Mild", 
    "Rainy", "Windy", "Sunny", "Cloudy", "Snowy", "Stormy",
    "Humid", "Dry"
]

# UPDATED: Two separate tag systems
# Occasion/Activity Tags (when/where to wear)
OCCASION_STYLE_TAGS = {
    "Core Dress Codes": ["Casual", "Formal", "Comfortable"],
    "Social Events": ["Party", "Date", "Wedding", "Cocktail"],
    "Daily Activities": ["Work", "Shopping", "Brunch", "Dinner", "Meeting", "Interview"],
    "Fitness & Sports": ["Sport", "Gym", "Yoga"],
    "Leisure": ["Beach", "Vacation", "Lounging", "Home"],
    "Entertainment": ["Festival", "Concert", "Theater", "Picnic"],
    "Celebrations": ["Birthday", "Graduation"]
}

# Mood/Aesthetic Tags (style/feeling of clothing)
MOOD_STYLE_TAGS = [
    "Streetwear", "Boho", "Vintage", "Classic", "Trendy", "Minimalist", 
    "Elegant", "Chic", "Edgy", "Romantic", "Preppy", "Sporty Chic", "Confident"
]

def get_all_occasion_tags():
    """Helper function to get all occasion tags as a flat list"""
    all_tags = []
    for category_tags in OCCASION_STYLE_TAGS.values():
        all_tags.extend(category_tags)
    return all_tags

def get_all_style_tags():
    """Helper function to get all style tags (both occasion and mood) as a flat list"""
    all_tags = []
    # Add occasion tags
    for category_tags in OCCASION_STYLE_TAGS.values():
        all_tags.extend(category_tags)
    # Add mood tags
    all_tags.extend(MOOD_STYLE_TAGS)
    return all_tags

def get_category_icon(category: str) -> str:
    """Get emoji icon for category"""
    category_icons = {
        'Shirt': "👔", 'T-shirt': "👕", 'Jeans': "👖", 'Jacket': "🧥", 
        'Sneakers': "👟", 'Dress': "👗", 'Tops': "👚", 'Bottoms': "👖",
        'Outerwear': "🧥", 'Shoes': "👠", 'Accessories': "👜", 
        'Activewear': "🏃‍♀️", 'Swimwear': "👙", 'Sleepwear': "👘"
    }
    return category_icons.get(category, "🧺")

IMAGE_FOLDER = os.path.join("assets", "images")

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
</style>
""", unsafe_allow_html=True)

# Ensure directory exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)

# ----------- CUSTOM GLOBAL STYLES -----------
st.markdown("""
<style>
    .subheading {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #4a2511;
        margin-bottom: 0.25em;
    }
    .wardrobe-form-card {
        background: #fefcfa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e8ddd4;
    }
    /* Sidebar background gradient */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;
    }
    /* Style tags expander styling */
    .style-tags-container {
        margin-top: 10px;
        margin-bottom: 15px;
    }
    /* Custom expander styling for better appearance */
    .streamlit-expanderHeader {
        background-color: #f8f4f0 !important;
        border-radius: 8px !important;
        border: 1px solid #e8ddd4 !important;
        margin-bottom: 5px !important;
    }
    /* Style the expander content */
    .streamlit-expanderContent {
        background-color: #fefcfa !important;
        border: 1px solid #e8ddd4 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

def wardrobe_page(db):
    """Wardrobe page with database parameter"""
    # Initialize database service with database connection
    global wardrobe_db
    wardrobe_db = WardrobeDatabase(db)
    
    username = st.session_state.username
    st.markdown("---")
    st.markdown("""
        <h1 style='font-size:2.25rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🧥 Your Wardrobe
        </h1>
    """, unsafe_allow_html=True)
    add_enhanced_item_form(username)
    show_wardrobe_management(username)

# V2 Wrapper functions to maintain compatibility
def get_user_wardrobe(username: str) -> list:
    return wardrobe_db.get_user_wardrobe(username)

def add_wardrobe_item(username: str, item_data: dict) -> bool:
    return wardrobe_db.add_wardrobe_item(username, item_data)

def update_wardrobe_item(username: str, item_id: int, item_data: dict) -> bool:
    return wardrobe_db.update_wardrobe_item(username, item_id, item_data)

def delete_wardrobe_item(username: str, item_id: int) -> bool:
    return wardrobe_db.delete_wardrobe_item(username, item_id)

def get_wardrobe_item_by_id(username: str, item_id: int) -> dict:
    return wardrobe_db.get_wardrobe_item_by_id(username, item_id)

def show_wardrobe_management(username):
    items = get_user_wardrobe(username)
    
    with st.sidebar:
        st.markdown("""<style>.css-1d391kg {
        background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;}
        section[data-testid="stSidebar"] > div {
        background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;}
        </style>""", unsafe_allow_html=True)

        st.markdown("""<h1 style='font-size:1.35rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🔍 Search & Filters</h1>""", unsafe_allow_html=True)
        search_query = st.text_input("Search items...", placeholder="e.g., blue shirt")
    
        st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🏷️ Filters</h1>""", unsafe_allow_html=True)
        weather_filter = st.multiselect("Weather Tags", WEATHER_TAGS, key="weather_filter")
        
        # NEW: Separate filters for occasion and mood tags
        occasion_filter = st.multiselect("📅 Occasion Tags", get_all_occasion_tags(), key="occasion_filter")
        mood_filter = st.multiselect("🎧 Mood Tags", MOOD_STYLE_TAGS, key="mood_filter")
    
        st.markdown("""<h1 style='font-size:1.25rem; font-weight:600; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        📂 Category Filter </h1>""", unsafe_allow_html=True) 
        selected_category = st.session_state.get('active_category', 'All')
    
        col_cat_all, = st.columns([1])
        if col_cat_all.button("All Items", key="cat_all_sidebar", use_container_width=True):
            st.session_state['active_category'] = 'All'
            st.rerun()
        
        for category in CATEGORIES.keys():
            if st.button(f"{get_category_icon(category)} {category}", key=f"cat_{category}_sidebar", use_container_width=True):
                st.session_state['active_category'] = category
                st.rerun()

    # Apply filters
    filtered_items = items.copy()
    
    # Search filter
    if search_query:
        filtered_items = [
            item for item in filtered_items
            if search_query.lower() in item.get("name", "").lower()
            or search_query.lower() in item.get("category", "").lower()
            or search_query.lower() in item.get("subcategory", "").lower()
        ]
    
    # Category filter
    selected_category = st.session_state.get('active_category', 'All')
    if selected_category != "All":
        filtered_items = [item for item in filtered_items if item.get("category") == selected_category]
    
    # Weather filter
    if weather_filter:
        filtered_items = [
            item for item in filtered_items
            if any(tag in item.get("weather_tags", []) for tag in weather_filter)
        ]
    
    # NEW: Occasion filter
    if occasion_filter:
        filtered_items = [
            item for item in filtered_items
            if any(tag in item.get("style_tags", []) for tag in occasion_filter)
        ]
    
    # NEW: Mood filter
    if mood_filter:
        filtered_items = [
            item for item in filtered_items
            if any(tag in item.get("style_tags", []) for tag in mood_filter)
        ]
    
    # Display items
    st.markdown("---")
    st.markdown("### 👔 Your Wardrobe Collection")
    
    if not filtered_items:
        st.info("📭 No items found. Try adjusting your filters or add some items!")
    else:
        cols_per_row = 3
        for i in range(0, len(filtered_items), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(filtered_items):
                    item = filtered_items[i + j]
                    with cols[j]:
                        show_item_card(username, item)
    
    st.markdown("---")

def show_item_card(username, item):
    # Prepare badges with improved display for two tag types
    if item.get("weather_tags"):
        weather_badge = (
            "<span style='color:#313131; padding:3px 10px;"
            "border-radius:12px; font-size:0.85rem; font-weight:600; margin-right:0.4em;'>"
            f"🌤️ {', '.join([t.title() for t in item['weather_tags']])}"
            "</span>"
        )
    else:
        weather_badge = ""
    
    # Separate occasion and mood tags for display on different lines
    occasion_tags = []
    mood_tags = []
    
    for tag in item.get("style_tags", []):
        if tag in get_all_occasion_tags():
            occasion_tags.append(tag)
        elif tag in MOOD_STYLE_TAGS:
            mood_tags.append(tag)
    
    # Create separate badge lines for occasion and mood tags
    occasion_badge = ""
    mood_badge = ""
    
    if occasion_tags:
        occasion_badge = (
            "<span style='color:#444; padding:3px 10px;"
            "border-radius:12px; font-size:0.85rem; font-weight:600; margin-right:0.4em;'>"
            f"📅 {', '.join([t.title() for t in occasion_tags])}"
            "</span>"
        )
    
    if mood_tags:
        mood_badge = (
            "<span style='color:#444; padding:3px 10px;"
            "border-radius:12px; font-size:0.85rem; font-weight:600;'>"
            f"🎧 {', '.join([t.title() for t in mood_tags])}"
            "</span>"
        )

    # Image block: fixed, square, centered
    image_html = ""
    if item.get("image") and os.path.exists(item["image"]):
        try:
            img = Image.open(item["image"])
            min_dim = min(img.size)
            left = (img.width - min_dim) // 2
            top = (img.height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            img_cropped = img.crop((left, top, right, bottom))
            img_cropped = img_cropped.resize((200, 200), Image.LANCZOS)
            buffered = BytesIO()
            img_cropped.save(buffered, format="PNG", quality=95)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_html = f"<img src='data:image/png;base64,{img_str}' style='width:200px; height:200px; object-fit:cover; display:block; margin:auto;'/>"
        except (FileNotFoundError, OSError, IOError) as e:
            st.warning(f"Could not load image: {str(e)}")
            image_html = "<div style='height:200px; width:200px; background:#f2f2f2; color:#888; display:flex; align-items:center; justify-content:center;'>📷</div>"
    else:
        image_html = "<div style='height:200px; width:200px; background:#f2f2f2; color:#888; display:flex; align-items:center; justify-content:center;'>📷</div>"

    # Create a container div that wraps both the card and buttons to ensure proper alignment
    st.markdown(f"""
        <div style='width: 100%; display: flex; flex-direction: column; align-items: center; margin-bottom: 1.5em;'>
            <div style='
                background: #fcf7ed;
                border-radius: 18px;
                box-shadow: 0 4px 15px #d4b29e20;
                margin-bottom: 0.8em;
                margin-top: 0.2em;
                padding: 1.1em 1em 0.95em 1.2em;
                width: 100%;
                max-width: 280px;
                min-height: 400px;
                box-sizing: border-box;
                overflow: auto;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                position: relative;
            '>
                {image_html}
                <div style='font-size:1.23rem; font-weight:800; color:#4a2511;
                             margin-bottom:3px; margin-top:5px;
                             overflow-wrap: break-word; max-width: 240px; text-align: center;'>
                    {item.get("name", "Unnamed Item")}
                </div>
                <div style='color:#7a5d42; font-weight:600; margin-bottom:0.5em; font-size:1.06rem;
                            overflow-wrap: break-word; max-width: 240px; text-align: center;'>
                    {item.get("category", "")} &bull; {item.get("subcategory", "")}
                </div>
                <div style='margin-bottom:4px; max-width:240px; text-align:left; overflow-wrap:break-word;
                            white-space: normal; line-height: 1.4;'>
                    <div style='margin-bottom: 5px;'>{weather_badge}</div>
                    <div style='margin-bottom: 3px;'>{occasion_badge}</div>
                    <div>{mood_badge}</div>
                </div>
                <div style='flex:1;'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Action buttons below the card - now properly aligned with the card width
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Edit", key=f"edit_{item.get('item_id')}", use_container_width=True, help="Edit item details"):
            st.session_state.editing_item = item.get('item_id')
            st.rerun()
    with col2:
        if st.button("🗑️ Delete", key=f"delete_{item.get('item_id')}", use_container_width=True, help="Delete this item"):
            if delete_wardrobe_item(username, item.get('item_id')):
                st.success("Item deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete item.")

def add_enhanced_item_form(username):
    editing_item_id = st.session_state.get("editing_item")
    editing_item = None
    if editing_item_id:
        editing_item = get_wardrobe_item_by_id(username, editing_item_id)
        if editing_item is None:
            st.session_state.editing_item = None
            st.rerun()

    st.markdown("""
        <h1 style='font-size:1.5rem; font-weight:500; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        📂 Add or Edit an Item
        </h1>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="wardrobe-form-card">', unsafe_allow_html=True)
    
    col_cat1, col_cat2 = st.columns(2)
    with col_cat1:
        st.markdown('<span style="font-weight:700">Category *</span>', unsafe_allow_html=True)
        selected_category = st.selectbox(
            "",
            list(CATEGORIES.keys()),
            index=list(CATEGORIES.keys()).index(editing_item.get('category', 'Shirt'))
            if editing_item and editing_item.get('category') in CATEGORIES else 0,
            key="category_selector",
            label_visibility='collapsed'
        )
    
    with col_cat2:
        st.markdown('<span style="font-weight:700">Subcategory *</span>', unsafe_allow_html=True)
        available_subcategories = CATEGORIES[selected_category]
        selected_subcategory = st.selectbox(
            "",
            available_subcategories,
            index=available_subcategories.index(
                editing_item.get('subcategory', available_subcategories[0])
            )
            if editing_item and editing_item.get('subcategory') in available_subcategories else 0,
            key="subcategory_selector",
            label_visibility='collapsed'
        )
    
    # Use unique form keys to prevent conflicts
    form_key = f"edit_item_form_{username}_{editing_item_id}" if editing_item else f"add_item_form_{username}"
    
    with st.form(form_key, clear_on_submit=not bool(editing_item)):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span style="font-weight:700">📋 Item Name *</span>', unsafe_allow_html=True)
            name = st.text_input(
                "",
                value=editing_item.get('name', '') if editing_item else '',
                placeholder="e.g., Blue Cotton T-Shirt",
                label_visibility='collapsed'
            )
            
            st.info(f"📂**Category:** {selected_category} • {selected_subcategory}")
            
            # File upload section - moved up and aligned with style tags in column 2
            st.markdown('<span style="font-weight:700">📷 Upload Image *</span>', unsafe_allow_html=True)
            if not editing_item:
                st.caption("📷 Maximum file size: 200MB. Supported formats: JPG, JPEG, PNG")
                image_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility='collapsed')
            else:
                st.markdown('<span style="font-weight:700">Current Image:</span>', unsafe_allow_html=True)
                if editing_item.get("image") and os.path.exists(editing_item["image"]):
                    try:
                        img = Image.open(editing_item["image"])
                        st.image(img, width=170)
                    except Exception as e:
                        st.write(f"Image unavailable: {str(e)}")
                st.caption("📷 Maximum file size: 200MB. Supported formats: JPG, JPEG, PNG")
                image_file = st.file_uploader("Replace Image (optional)", type=["jpg", "jpeg", "png"])
        
        with col2:
            st.markdown('<span style="font-weight:700">🌤️ Weather Suitability</span>', unsafe_allow_html=True)
            st.caption("Select weather conditions where this item is appropriate")
            st.markdown('<span> Weather Tags *</span>', unsafe_allow_html=True)
            weather_tags = st.multiselect(
                "",
                WEATHER_TAGS,
                default=editing_item.get('weather_tags', []) if editing_item else [],
                help="Choose weather conditions this item is suitable for",
                label_visibility='collapsed'
            )
            
            # NEW: Two-category style tag system
            st.markdown('<span style="font-weight:700">👗 Style & Occasion</span>', unsafe_allow_html=True)
            st.caption("Select occasions and mood/aesthetic for this item")
            
            # Get current tags for editing
            current_occasion_tags = []
            current_mood_tags = []
            if editing_item and editing_item.get('style_tags'):
                for tag in editing_item.get('style_tags', []):
                    if tag in get_all_occasion_tags():
                        current_occasion_tags.append(tag)
                    elif tag in MOOD_STYLE_TAGS:
                        current_mood_tags.append(tag)
            
            # Occasion tags selection
            st.markdown('<span>📅 Occasion Tags *</span>', unsafe_allow_html=True)
            occasion_tags = st.multiselect(
                "",
                get_all_occasion_tags(),
                default=current_occasion_tags,
                help="Choose occasions and activities for this item",
                label_visibility='collapsed',
                key="occasion_multiselect"
            )
            
            # Mood/Aesthetic tags selection
            st.markdown('<span>🎧 Mood/Aesthetic Tags *</span>', unsafe_allow_html=True)
            mood_tags = st.multiselect(
                "",
                MOOD_STYLE_TAGS,
                default=current_mood_tags,
                help="Choose the mood or aesthetic style of this item",
                label_visibility='collapsed',
                key="mood_multiselect"
            )
            
            # Combine both tag types for final style_tags
            style_tags = occasion_tags + mood_tags
        
        st.info("💡 **Tip:** Select both occasion and mood tags to make your outfit recommendations more accurate!")
        
        # Form buttons
        if editing_item:
            col_spacer1, col_submit, col_cancel, col_spacer2 = st.columns([1, 1, 1, 1])
            with col_submit:
                submitted = st.form_submit_button("💾 Update Item", use_container_width=True)
            with col_cancel:
                if st.form_submit_button("❌ Cancel Edit", use_container_width=True):
                    st.session_state.editing_item = None
                    st.rerun()
        else:
            col_spacer1, col_submit, col_spacer2 = st.columns([1, 2, 1])
            with col_submit:
                submitted = st.form_submit_button("╰┈➤🚪 Add to Wardrobe", use_container_width=True)
        
        # Form submission handling
        if submitted:
            if not name.strip():
                st.error("Please enter an item name.")
            elif not weather_tags:
                st.error("Please select at least one weather tag.")
            elif not occasion_tags and not mood_tags:
                st.error("Please select at least one occasion tag or mood tag.")
            elif not editing_item and not image_file:
                st.error("Please upload an image.")
            else:
                try:
                    image_path = None
                    if image_file is not None:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{timestamp}_{username}_{image_file.name}"
                        image_path = os.path.join(IMAGE_FOLDER, filename)
                        with open(image_path, "wb") as f:
                            f.write(image_file.getbuffer())
                    elif editing_item:
                        image_path = editing_item.get("image", "")
                    
                    item_data = {
                        "name": name.strip(),
                        "category": selected_category,
                        "subcategory": selected_subcategory,
                        "weather_tags": weather_tags,
                        "style_tags": style_tags,  # This now contains both occasion and mood tags
                        "image": image_path,
                        "added_at": editing_item.get("added_at", datetime.now().isoformat()) if editing_item else datetime.now().isoformat()
                    }
                    
                    if editing_item:
                        if update_wardrobe_item(username, editing_item_id, item_data):
                            st.success("🎉 Item updated successfully!")
                            st.session_state.editing_item = None
                            st.rerun()
                        else:
                            st.error("Failed to update item.")
                    else:
                        if add_wardrobe_item(username, item_data):
                            st.success("🎉 Item added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add item.")
                            
                except Exception as e:
                    st.error(f"Error processing item: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
