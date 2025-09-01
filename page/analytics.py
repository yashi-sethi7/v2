import streamlit as st


# V2 Database operations for analytics
class AnalyticsDatabase:
    """Database operations for wardrobe analytics in V2"""
    
    def __init__(self, db):
        self.db = db
    
    def get_wardrobe_analytics(self, username: str) -> dict:
        """Get comprehensive wardrobe analytics from database"""
        try:
            # Get all wardrobe items for the user
            query = """
                SELECT wi.*, u.username 
                FROM wardrobe_items wi 
                JOIN users u ON wi.user_id = u.user_id 
                WHERE u.username = %s
            """
            items = self.db.fetch_all(query, (username,))
            
            if not items:
                return {
                    "total_items": 0,
                    "category_distribution": {},
                    "weather_distribution": {},
                    "style_distribution": {},
                    "missing_weather_coverage": [],
                    "missing_style_coverage": []
                }
            
            # Process analytics data
            total_items = len(items)
            category_distribution = {}
            weather_distribution = {}
            style_distribution = {}
            
            # Count categories
            for item in items:
                category = item.get('category', 'Unknown')
                category_distribution[category] = category_distribution.get(category, 0) + 1
            
            # Count weather tags
            for item in items:
                weather_tags = item.get('weather_tags', '')
                if weather_tags:
                    tags = [tag.strip().lower() for tag in weather_tags.split(',') if tag.strip()]
                    for tag in tags:
                        weather_distribution[tag] = weather_distribution.get(tag, 0) + 1
            
            # Count style tags
            for item in items:
                style_tags = item.get('style_tags', '')
                if style_tags:
                    tags = [tag.strip().lower() for tag in style_tags.split(',') if tag.strip()]
                    for tag in tags:
                        style_distribution[tag] = style_distribution.get(tag, 0) + 1
            
            # Calculate missing coverage
            all_weather_tags = {tag.lower() for tag in WEATHER_TAGS}
            all_style_tags = {tag.lower() for tag in get_all_style_tags()}
            
            missing_weather = list(all_weather_tags - set(weather_distribution.keys()))
            missing_style = list(all_style_tags - set(style_distribution.keys()))
            
            return {
                "total_items": total_items,
                "category_distribution": category_distribution,
                "weather_distribution": weather_distribution,
                "style_distribution": style_distribution,
                "missing_weather_coverage": missing_weather,
                "missing_style_coverage": missing_style
            }
            
        except Exception as e:
            st.error(f"Error loading analytics: {e}")
            return {
                "total_items": 0,
                "category_distribution": {},
                "weather_distribution": {},
                "style_distribution": {},
                "missing_weather_coverage": [],
                "missing_style_coverage": []
            }


# Weather tags from optimized list (from wardrobe.py)
WEATHER_TAGS = [
    "Hot", "Cold", "Freezing", "Mild", 
    "Rainy", "Windy", "Sunny", "Cloudy", "Snowy", "Stormy",
    "Humid", "Dry"
]

# Style tags from categorized system (from wardrobe.py)
STYLE_TAGS_CATEGORIES = {
    "Core Dress Codes": ["Casual", "Formal", "Comfortable"],
    "Social Events": ["Party", "Date", "Wedding", "Cocktail"],
    "Daily Activities": ["Work", "Shopping", "Brunch", "Dinner", "Meeting", "Interview"],
    "Fitness & Sports": ["Sport", "Gym", "Yoga"],
    "Leisure": ["Beach", "Vacation", "Lounging", "Home"],
    "Entertainment": ["Festival", "Concert", "Theater", "Picnic"],
    "Celebrations": ["Birthday", "Graduation"],
    "Style Aesthetics": ["Streetwear", "Boho", "Vintage", "Classic", "Trendy", "Minimalist", "Elegant", "Chic", "Edgy", "Romantic", "Preppy", "Sporty Chic"]
}

def get_all_style_tags():
    """Helper function to get all style tags as a flat list"""
    all_tags = []
    for category_tags in STYLE_TAGS_CATEGORIES.values():
        all_tags.extend(category_tags)
    return all_tags

# For compatibility, create flat STYLE_TAGS list
STYLE_TAGS = get_all_style_tags()

# --- Custom CSS for container cards, badges, and buttons (PRESERVED EXACTLY) ---
st.markdown("""
    <style>
        .analytics-hero {
            background: linear-gradient(95deg, #eed6d3 60%, #a26769 100%);
            border-radius: 22px;
            padding: 2rem 2.3rem;
            margin-top: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 25px rgba(161,130,91,0.3);
            font-family: 'Montserrat', sans-serif;
        }
        .analytics-header {
            font-size: 2.3rem;
            color: #4a2511;
            font-weight: 900;
            letter-spacing: 2.5px;
            margin-bottom: 5px;
            text-align: center;
        }
        .analytics-subtitle {
            font-size: 1.1rem;
            font-style: italic;
            color: #7F5A5A;
            text-align: center;
            margin-bottom: 1.8rem;
        }
        .metric-card {
            background: #f9f5ee;
            border-radius: 20px;
            padding: 1.3rem 1rem;
            box-shadow: 0 6px 15px rgba(161,130,91,0.15);
            text-align: center;
            font-weight: 700;
            color: #4a2511;
            margin-bottom: 0.5rem;
        }
        .analytics-section {
            background: #fcf7ed;
            padding: 1.6rem 2rem;
            border-radius: 18px;
            margin-bottom: 2rem;
            box-shadow: 0 6px 22px rgba(204, 167, 127, 0.18);
        }
        .analytics-section h3 {
            color: #7f5a5a;
            font-weight: 700;
            margin-bottom: 0.8rem;
            border-bottom: 1px solid #d4b29e;
            padding-bottom: 6px;
        }
        .list-inline {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem 1.2rem;
            margin-top: 0.3rem;
        }
        .list-inline span {
            background: #d4b29e;
            color: #4a2511;
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.95rem;
            user-select: none;
        }
        .alert-warning {
            background: #fcece7;
            border-left: 6px solid #a26769;
            color: #7f5a5a;
            padding: 1rem 1.2rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .alert-success {
            background: #e9f5ea;
            border-left: 6px solid #5c9e70;
            color: #39683a;
            padding: 1rem 1.2rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .recommendations {
            font-weight: 600;
            color: #4a2511;
            margin-left: 0.7rem;
            margin-bottom: 0.6rem;
        }
        .btn-refresh {
            background: linear-gradient(90deg, #a26769 60%, #e0c7a3 120%);
            color: white;
            font-weight: 700;
            padding: 8px 24px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 5px 12px rgba(162, 103, 105, 0.5);
            margin-bottom: 1.6rem;
            transition: background 0.3s ease;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .btn-refresh:hover {
            background: linear-gradient(90deg, #7f5656 20%, #cbb090 100%);
        }
    </style>
""", unsafe_allow_html=True)

def analytics_page(db):
    """Analytics page with database parameter"""
    # Initialize database service with database connection
    global analytics_db
    analytics_db = AnalyticsDatabase(db)
    
    username = st.session_state.username

    st.markdown("""
        <h1 style='font-size:2rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        📊 Analytics & Insights
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color:#7b5155;font-size:1.08rem;'>🧠 Know your wardrobe better — Category, Tag coverage & Missing pieces</p>", 
    unsafe_allow_html=True)
    
    analytics = get_wardrobe_analytics(username)

    if not analytics or analytics.get("total_items", 0) == 0:
        st.info("📭 Your wardrobe is empty. Add items to unlock analytics.")
        return

    # Updated refresh button (using st.rerun() instead of deprecated experimental_rerun)
    if st.button("Refresh Analytics", key="refresh_analytics", help="Refresh analytics data"):
        st.rerun()

    # --- OVERVIEW METRICS (guaranteed horizontal using columns) (PRESERVED EXACTLY) ---
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(
        f'<div class="metric-card">Total Items<br><span style="color:#7b5155;font-size:1.8rem; font-weight:900;">{analytics["total_items"]}</span></div>',
        unsafe_allow_html=True)
    coverage_weather = f'{len(analytics["weather_distribution"])}/{len(WEATHER_TAGS)}'
    col2.markdown(
        f'<div class="metric-card">Weather Coverage<br><span style="color:#7b5155;font-size:1.8rem; font-weight:900;">{coverage_weather}</span></div>',
        unsafe_allow_html=True)
    coverage_style = f'{len(analytics["style_distribution"])}/{len(STYLE_TAGS)}'
    col3.markdown(
        f'<div class="metric-card">Style Coverage<br><span style="color:#7b5155;font-size:1.8rem; font-weight:900;">{coverage_style}</span></div>',
        unsafe_allow_html=True)
    coverage_cat = len(analytics["category_distribution"])
    col4.markdown(
        f'<div class="metric-card">Categories<br><span style="color:#7b5155;font-size:1.8rem; font-weight:900;">{coverage_cat}</span></div>',
        unsafe_allow_html=True)

    # Detailed Analytics in two columns (PRESERVED EXACTLY)
    colL, colR = st.columns(2)

    with colL:
        st.markdown("""
        <h1 style='font-size:1.7rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🌤️ Weather Tag Distribution
        </h1>
    """, unsafe_allow_html=True)
        if analytics["weather_distribution"]:
            tags_line = ' '.join(
                f'<span>{tag.title()} ({count})</span>'
                for tag, count in sorted(analytics["weather_distribution"].items(), key=lambda x: x[1], reverse=True)
            )
            st.markdown(f'<div class="list">{tags_line}</div>', unsafe_allow_html=True)
        else:
            st.write("No weather tags yet")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <h1 style='font-size:1.7rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        🎯 Wardrobe Gaps
        </h1>
    """, unsafe_allow_html=True)
        if analytics["missing_weather_coverage"]:
            weather_list = '<br>'.join(f'- {tag.title()}' for tag in analytics["missing_weather_coverage"])
            st.markdown(
                f"""<div class="alert-warning"><b>Missing Weather Coverage:</b><br>{weather_list}</div>""",
                unsafe_allow_html=True)
        if analytics["missing_style_coverage"]:
            style_list = '<br>'.join(f'- {tag.title()}' for tag in analytics["missing_style_coverage"])
            st.markdown(
                f"""<div class="alert-warning"><b>Missing Style Coverage:</b><br>{style_list}</div>""",
                unsafe_allow_html=True)
        if not analytics["missing_weather_coverage"] and not analytics["missing_style_coverage"]:
            st.success("🎉 Complete coverage across all tags!")
        st.markdown("</div>", unsafe_allow_html=True)

    with colR:
        st.markdown("""
        <h1 style='font-size:1.7rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        👗 Style Tag Distribution
        </h1>
    """, unsafe_allow_html=True)
        if analytics["style_distribution"]:
            tags_line = ' '.join(
                f'<span>{tag.title()} ({count})</span>'
                for tag, count in sorted(analytics["style_distribution"].items(), key=lambda x: x[1], reverse=True)
            )
            st.markdown(f'<div class="list">{tags_line}</div>', unsafe_allow_html=True)
        else:
            st.write("No style tags yet")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <h1 style='font-size:1.7rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        📁 Category Distribution
        </h1>
    """, unsafe_allow_html=True)
        if analytics["category_distribution"]:
            tags_line = ' '.join(
                f'<span>{category} ({count})</span>'
                for category, count in sorted(analytics["category_distribution"].items(), key=lambda x: x[1], reverse=True)
            )
            st.markdown(f'<div class="list">{tags_line}</div>', unsafe_allow_html=True)
        else:
            st.write("No categories found")
        st.markdown("</div>", unsafe_allow_html=True)

    # Recommendations Section (PRESERVED EXACTLY)
    st.markdown("""
        <h1 style='font-size:1.7rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        💡 Smart Recommendations
        </h1>
    """, unsafe_allow_html=True)
    recommendations = []

    if "cold" in analytics.get("missing_weather_coverage", []):
        recommendations.append("🧥 Consider adding winter coats or warm sweaters for cold weather")
    if "hot" in analytics.get("missing_weather_coverage", []):
        recommendations.append("☀️ Add light, breathable items for hot weather")
    if "rainy" in analytics.get("missing_weather_coverage", []):
        recommendations.append("🌧️ Consider waterproof jackets or rain-friendly shoes")
    if "formal" in analytics.get("missing_style_coverage", []):
        recommendations.append("👔 Add formal wear for office and business occasions")
    if "party" in analytics.get("missing_style_coverage", []):
        recommendations.append("🎉 Consider adding party outfits for special events")
    if "casual" in analytics.get("missing_style_coverage", []):
        recommendations.append("👕 Add more casual, everyday comfortable pieces")
    
    categories = analytics.get("category_distribution", {})
    if categories.get("Tops", 0) > 2 * categories.get("Bottoms", 0):
        recommendations.append("👖 Consider adding more bottoms to balance your wardrobe")
    if categories.get("Bottoms", 0) > 2 * categories.get("Tops", 0):
        recommendations.append("👕 Consider adding more tops to balance your wardrobe")
    
    if recommendations:
        for rec in recommendations[:5]:
            st.markdown(f'<div class="recommendations">• {rec}</div>', unsafe_allow_html=True)
    else:
        st.success("🌟 Your wardrobe looks well-balanced!")

    st.markdown('</div>', unsafe_allow_html=True)

# V2 Wrapper function to maintain compatibility
def get_wardrobe_analytics(username: str) -> dict:
    """V2 database wrapper for get_wardrobe_analytics"""
    return analytics_db.get_wardrobe_analytics(username)

# Main execution
if __name__ == "__main__":
    from config.database import get_database
    db = get_database()
    analytics_page(db)
