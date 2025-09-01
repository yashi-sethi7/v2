import streamlit as st
from PIL import Image
import os
from datetime import datetime


# V2 Database operations for outfit generator
class OutfitGeneratorDatabase:
    """Database operations for outfit generation and management in V2"""
    
    def __init__(self, db):
        self.db = db
    
    def get_user_wardrobe(self, username: str) -> list:
        """Get user's wardrobe items from database for outfit generation"""
        try:
            query = """
                SELECT wi.*, u.username 
                FROM wardrobe_items wi 
                JOIN users u ON wi.user_id = u.user_id 
                WHERE u.username = %s 
                ORDER BY wi.created_at DESC
            """
            items = self.db.fetch_all(query, (username,))
            
            # Convert database format to outfit generator format
            formatted_items = []
            for item in items:
                formatted_item = {
                    'item_id': item['id'],  # FIXED: Use 'id' instead of 'item_id'
                    'name': item['name'],   # FIXED: Use 'name' instead of 'item_name'
                    'category': item['category'],
                    'subcategory': item.get('subcategory', ''),  # FIXED: Use 'subcategory' not 'subcategory_id'
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
    
    def save_outfit(self, username: str, outfit_data: dict) -> bool:
        """Save generated outfit to database"""
        try:
            # Get user_id from username
            user_result = self.db.fetch_one("SELECT user_id FROM users WHERE username = %s", (username,))
            if not user_result:
                st.error("User not found")
                return False
            
            user_id = user_result['user_id']
            
            # Generate outfit name
            outfit_name = f"Generated Outfit {datetime.now().strftime('%m/%d %H:%M')}"
            
            # FIXED: Insert outfit with correct column names
            outfit_query = """
                INSERT INTO outfits (user_id, name, occasion, season, compatibility_score, weather_condition, event_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            outfit_id = self.db.insert_data(outfit_query, (
                user_id, 
                outfit_name,
                outfit_data.get('event_type', ''),
                outfit_data.get('weather', ''),
                outfit_data.get('compatibility_score', 0),
                outfit_data.get('weather', ''),
                outfit_data.get('event_type', '')
            ))
            
            if not outfit_id:
                return False
            
            # FIXED: Insert outfit items with correct column names
            for item in outfit_data.get('items', []):
                self.db.insert_data(
                    "INSERT INTO outfit_items (outfit_id, wardrobe_item_id) VALUES (%s, %s)",
                    (outfit_id, item.get('item_id'))
                )
            
            return True
        except Exception as e:
            st.error(f"Error saving outfit: {e}")
            return False
    
    def enhanced_generate_outfit(self, wardrobe_items: list, weather: str, event_type: str, day: str) -> list:
        """Enhanced outfit generation with compatibility scoring"""
        if not wardrobe_items:
            return []
        
        # Define outfit structure requirements
        required_categories = ['Tops', 'Bottoms']  # Minimum required
        optional_categories = ['Outerwear', 'Shoes', 'Accessories']  # Nice to have
        
        # Filter items by weather compatibility
        weather_compatible_items = []
        for item in wardrobe_items:
            item_weather_tags = [tag.lower() for tag in item.get('weather_tags', [])]
            if weather.lower() in item_weather_tags or not item_weather_tags:
                weather_compatible_items.append(item)
        
        # Filter by style/event compatibility
        style_compatible_items = []
        for item in weather_compatible_items:
            item_style_tags = [tag.lower() for tag in item.get('style_tags', [])]
            event_lower = event_type.lower()
            
            # Check if item style matches event
            if (event_lower in item_style_tags or 
                'casual' in item_style_tags and event_lower in ['weekend', 'shopping'] or
                'formal' in item_style_tags and event_lower in ['work', 'meeting'] or
                not item_style_tags):  # Include items with no style tags
                style_compatible_items.append(item)
        
        if len(style_compatible_items) < 2:
            return []
        
        # Group items by category
        items_by_category = {}
        for item in style_compatible_items:
            category = item.get('category', 'Other')
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)
        
        # Generate outfit combinations
        outfits = []
        max_outfits = 3
        
        # Try to create outfits with required categories
        for top in items_by_category.get('Tops', []):
            for bottom in items_by_category.get('Bottoms', []):
                if len(outfits) >= max_outfits:
                    break
                
                outfit_items = [top, bottom]
                
                # Add optional items if available
                for category in optional_categories:
                    if category in items_by_category and items_by_category[category]:
                        # Take the first compatible item from each optional category
                        outfit_items.append(items_by_category[category][0])
                
                # Calculate compatibility score
                compatibility_score = self.calculate_compatibility_score(
                    outfit_items, weather, event_type, day
                )
                
                outfit = {
                    'items': outfit_items,
                    'compatibility_score': compatibility_score,
                    'weather': weather,
                    'event_type': event_type,
                    'day': day
                }
                outfits.append(outfit)
        
        # Sort by compatibility score (highest first)
        outfits.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return outfits[:max_outfits]
    
    def calculate_compatibility_score(self, items: list, weather: str, event_type: str, day: str) -> int:
        """Calculate outfit compatibility score"""
        base_score = 60  # Base score for having required items
        
        weather_match_count = 0
        style_match_count = 0
        total_items = len(items)
        
        for item in items:
            # Weather compatibility
            item_weather_tags = [tag.lower() for tag in item.get('weather_tags', [])]
            if weather.lower() in item_weather_tags:
                weather_match_count += 1
            
            # Style compatibility
            item_style_tags = [tag.lower() for tag in item.get('style_tags', [])]
            event_lower = event_type.lower()
            if (event_lower in item_style_tags or 
                'casual' in item_style_tags and event_lower in ['weekend', 'shopping'] or
                'formal' in item_style_tags and event_lower in ['work', 'meeting']):
                style_match_count += 1
        
        # Calculate bonus scores
        weather_bonus = (weather_match_count / total_items) * 25 if total_items > 0 else 0
        style_bonus = (style_match_count / total_items) * 15 if total_items > 0 else 0
        
        # Bonus for complete outfit (more than just top + bottom)
        completeness_bonus = 5 if total_items > 2 else 0
        
        final_score = int(base_score + weather_bonus + style_bonus + completeness_bonus)
        return min(final_score, 100)  # Cap at 100%


# Options for form inputs (maintain your existing options)
WEATHER_OPTIONS = [
    "Hot", "Cold", "Freezing", "Mild", 
    "Rainy", "Windy", "Sunny", "Cloudy", "Snowy", "Stormy",
    "Humid", "Dry"
]

EVENT_OPTIONS = [
    "Casual", "Formal", "Comfortable",
    "Party", "Date", "Wedding", "Cocktail",
    "Work", "Shopping", "Brunch", "Dinner", "Meeting", "Interview",
    "Sport", "Gym", "Yoga",
    "Beach", "Vacation", "Lounging", "Home",
    "Festival", "Concert", "Theater", "Picnic",
    "Birthday", "Graduation"
]

DAYS_OF_WEEK = [
    "Monday", "Tuesday", "Wednesday", "Thursday", 
    "Friday", "Saturday", "Sunday"
]

# ------- GLOBAL STYLING FOR THIS PAGE (PRESERVED EXACTLY) ------
st.markdown("""
    <style>
        .generator-header {
            font-size: 2.2rem !important;
            font-weight: 700;
            color: #4a2511;
            letter-spacing: 0.01em;
            margin-bottom: 0.1em;
        }
        .outfit-card {
            background: #f8f6f2e8;
            border-radius: 1.4rem;
            box-shadow: 0 2px 19px #cdb5991a;
            padding: 1.5rem 1.3rem 1.2rem 1.3rem;
            margin-bottom: 1.7rem;
            min-height: 240px;
        }
        .compatibility-score {
            background: linear-gradient(90deg, #a26769 55%, #e0c3a3 120%);
            color: #fff;
            font-weight: 670;
            border-radius: 18px;
            display: inline-block;
            padding: 0.45em 1.1em;
            font-size: 1.11rem;
            margin: 0.1em auto 0.58em auto;
            box-shadow: 0 1px 6px #eccdb652;
        }
        .stButton>button {
            border-radius: 24px !important;
            background: linear-gradient(90deg, #a26769 55%, #e0c3a3 120%);
            color: #fff;
            font-weight: 600;
            font-size: 1.01rem;
            border: 0;
            box-shadow: 0 2px 6px #dac2c224;
            margin-bottom: 0.16em;
            margin-top: 0.17em;
            transition: background 0.18s;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #7f5a5a 12%, #cbb7a6 90%);
        }
        .form-card {
            background: #faf7f2cc;
            border-radius: 17px;
            box-shadow: 0 2px 14px #dec8ad1f;
            padding: 1.2rem 1.55rem 0.5rem 1.55rem;
            margin-bottom: 1.4em;
        }
        .item-name {
            font-size: 1.06rem;
            font-weight: 650;
            color: #7b5155;
        }
        .item-subcat {
            font-size: 1rem;
            color: #a49283;
        }
        .item-tag-weather {
            color: #b75129;
            font-size: .99rem;
        }
        .item-tag-style {
            color: #8895b4;
            font-size: .99rem;
        }
        
        /* Stylish item boxes */
        .item-box {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 3px 12px rgba(224, 195, 163, 0.15);
            padding: 1rem;
            margin-bottom: 0.5rem;
            border: 1px solid #f0ebe5;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .item-box:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(224, 195, 163, 0.25);
            border-color: #e0c3a3;
        }
        
        .item-image-container {
            background: #faf8f5;
            border-radius: 8px;
            padding: 0.5rem;
            margin-bottom: 0.8rem;
            border: 1px solid #f5f1ec;
        }
        
        /* Image styling within boxes */
        .stImage {
            text-align: center;
            margin-bottom: 0;
        }
        
        .stImage > img {
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(116, 81, 85, 0.1);
        }
        
        /* Item details styling */
        .item-details {
            padding-top: 0.3rem;
            border-top: 1px solid #f0ebe5;
            margin-top: 0.5rem;
        }
        
        /* Tags styling within boxes */
        .item-tags {
            margin-top: 0.5rem;
            padding: 0.3rem;
            background: #faf8f5;
            border-radius: 6px;
            font-size: 0.85rem;
        }
        
        /* Ensure columns are equal height */
        .stColumn > div {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
    </style>
""", unsafe_allow_html=True)

def display_outfit_card(outfit, idx, username, button_prefix="save_outfit"):
    """Display a single outfit card with save functionality (PRESERVED EXACTLY)"""
    st.markdown(f'<div class="outfit-card">', unsafe_allow_html=True)
    
    # Header and score
    col_header, col_score = st.columns([3, 1])
    with col_header:
        st.markdown(f"<h4 style='margin-bottom:0.08em;'>👗 Outfit Option {idx + 1}</h4>", unsafe_allow_html=True)
    with col_score:
        score = outfit.get("compatibility_score", 0)
        st.markdown(f'<div class="compatibility-score">Match: {score}%</div>', unsafe_allow_html=True)

    # Display outfit items in stylish boxes
    cols = st.columns(len(outfit["items"]))
    for item_idx, item in enumerate(outfit["items"]):
        with cols[item_idx]:
            # Start of stylish item box
            st.markdown('<div class="item-box">', unsafe_allow_html=True)
            
            # Image container
            st.markdown('<div class="item-image-container">', unsafe_allow_html=True)
            
            if item.get("image") and os.path.exists(item["image"]):
                try:
                    img = Image.open(item["image"])
                    
                    # Standard dimensions
                    target_width = 150
                    target_height = 200
                    
                    # Calculate aspect ratios
                    original_aspect = img.width / img.height
                    target_aspect = target_width / target_height
                    
                    if original_aspect > target_aspect:
                        # Image is wider - fit by height, crop width
                        new_height = target_height
                        new_width = int(target_height * original_aspect)
                        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Crop to center
                        left = (new_width - target_width) // 2
                        img_final = img_resized.crop((left, 0, left + target_width, target_height))
                    else:
                        # Image is taller - fit by width, crop height
                        new_width = target_width
                        new_height = int(target_width / original_aspect)
                        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Crop to center
                        top = (new_height - target_height) // 2
                        img_final = img_resized.crop((0, top, target_width, top + target_height))
                    
                    st.image(img_final, width=target_width)
                    
                except Exception:
                    # Placeholder for errors
                    placeholder = Image.new('RGB', (150, 200), color=(245, 241, 236))
                    st.image(placeholder, width=150)
                    st.write('<span style="color:#c99794; font-size:0.9rem;">📷 Image unavailable</span>', unsafe_allow_html=True)
            else:
                # Create a placeholder image for missing images
                placeholder = Image.new('RGB', (150, 200), color=(245, 241, 236))
                st.image(placeholder, width=150)
                st.write('<span style="color:#c99794; font-size:0.9rem;">📷 No image</span>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)  # Close image container
            
            # Item details section
            st.markdown('<div class="item-details">', unsafe_allow_html=True)
            st.write(f'<span class="item-name">{item.get("name", "Unknown")}</span>', unsafe_allow_html=True)
            st.write(f'<span class="item-subcat">*{item.get("subcategory", "Unknown")}*</span>', unsafe_allow_html=True)
            
            # Tags section in a styled container
            weather_tags = item.get('weather_tags', [])
            style_tags = item.get('style_tags', [])
            if weather_tags or style_tags:
                st.markdown('<div class="item-tags">', unsafe_allow_html=True)
                tag_parts = []
                if weather_tags:
                    tag_parts.append(f'<span class="item-tag-weather">🌤️ {", ".join(weather_tags[:2])}</span>')
                if style_tags:
                    tag_parts.append(f'<span class="item-tag-style">👗 {", ".join(style_tags[:2])}</span>')
                st.markdown("<br>".join(tag_parts), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)  # Close tags container
            
            st.markdown('</div>', unsafe_allow_html=True)  # Close item details
            st.markdown('</div>', unsafe_allow_html=True)  # Close item box

    # Save button
    col1, col2 = st.columns([3, 1])
    with col2:
        button_key = f"{button_prefix}_{idx}_{hash(str(outfit))}"
        if st.button("💾 Save Outfit", key=button_key, help="Save this outfit to your collection"):
            outfit_to_save = dict(outfit)
            
            # Simple save without debug info
            if save_outfit(username, outfit_to_save):
                st.success("🎉 Outfit saved successfully!")
                # Clear generated outfits and refresh
                st.session_state["outfits_generated"] = False
                st.session_state["suggested_outfits"] = []
                st.rerun()
            else:
                st.error("❌ Failed to save outfit. Please try again.")
                
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

def generator_page(db):
    """Generator page with database parameter"""
    # Initialize database service with database connection
    global outfit_db
    outfit_db = OutfitGeneratorDatabase(db)
    
    st.markdown("""
        <h1 style='font-size:2rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        📦 Enhanced Smart Outfit Generator
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color:#7b5155;font-size:1.08rem;'>Get AI-powered outfit suggestions with compatibility scores!</p>", unsafe_allow_html=True)
    username = st.session_state.username

    wardrobe_items = get_user_wardrobe(username)

    if not wardrobe_items:
        st.warning("📭 You need to add some items to your wardrobe first!")
        st.markdown('<span style="color:#a26769; font-size:1.07rem;">👆 Go to the <b>Wardrobe</b> tab to add your clothing items with structured tags.</span>', unsafe_allow_html=True)
        return

    # ---- INPUT FORM ----
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("outfit_generator_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_weather = st.selectbox("🌤️ Weather", WEATHER_OPTIONS)
            with col2:
                selected_event = st.selectbox("🎭 Event Type", EVENT_OPTIONS)
            with col3:
                selected_day = st.selectbox("📅 Day", DAYS_OF_WEEK)
            generate_button = st.form_submit_button("🛒 Generate Smart Outfits", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- GENERATE & RESULT DISPLAY ----
    if generate_button:
        with st.spinner("🎨 Creating perfect outfits with AI matching..."):
            suggested_outfits = enhanced_generate_outfit(
                wardrobe_items, selected_weather, selected_event, selected_day
            )
            st.session_state["suggested_outfits"] = suggested_outfits
            st.session_state["outfits_generated"] = True

        if suggested_outfits:
            st.markdown(f"<h3 style='font-size:1.32rem; color:#4a2511;'>🎯 Smart Outfit Suggestions for {selected_day}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#594339;'><b>Weather:</b> {selected_weather} &nbsp; | &nbsp; <b>Event:</b> {selected_event}</span>", unsafe_allow_html=True)
            st.markdown("")
            
            # Display generated outfits
            for idx, outfit in enumerate(suggested_outfits):
                display_outfit_card(outfit, idx, username, "generate_save")
                
        else:
            st.warning("😔 Couldn't generate suitable outfits.")
            st.info("💡 Try adding more items with relevant weather and style tags.")

    # Show persisted outfits if they exist
    elif st.session_state.get("outfits_generated") and st.session_state.get("suggested_outfits"):
        suggested_outfits = st.session_state["suggested_outfits"]
        st.markdown(f"<h3 style='font-size:1.32rem; color:#4a2511;'>🎯 Your Generated Outfits</h3>", unsafe_allow_html=True)
        
        # Display persisted outfits
        for idx, outfit in enumerate(suggested_outfits):
            display_outfit_card(outfit, idx, username, "persist_save")

# V2 Wrapper functions to maintain compatibility
def get_user_wardrobe(username: str) -> list:
    """V2 database wrapper for get_user_wardrobe"""
    return outfit_db.get_user_wardrobe(username)

def enhanced_generate_outfit(wardrobe_items: list, weather: str, event_type: str, day: str) -> list:
    """V2 database wrapper for enhanced_generate_outfit"""
    return outfit_db.enhanced_generate_outfit(wardrobe_items, weather, event_type, day)

def save_outfit(username: str, outfit_data: dict) -> bool:
    """V2 database wrapper for save_outfit"""
    return outfit_db.save_outfit(username, outfit_data)

# Main execution
if __name__ == "__main__":
    from config.database import get_database
    db = get_database()
    generator_page(db)
