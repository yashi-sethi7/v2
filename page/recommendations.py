import streamlit as st
from datetime import datetime
import random
from collections import Counter


# V2 Database operations for recommendations
class RecommendationsDatabase:
    """Database operations for AI-powered outfit recommendations in V2"""
    
    def __init__(self, db):
        self.db = db
    
    def get_user_wardrobe_analytics(self, username: str) -> dict:
        """Get comprehensive wardrobe data for recommendations"""
        try:
            query = """
                SELECT wi.*, u.username 
                FROM wardrobe_items wi 
                JOIN users u ON wi.user_id = u.user_id 
                WHERE u.username = %s
            """
            items = self.db.fetch_all(query, (username,))
            
            if not items:
                return {'items': [], 'categories': {}, 'weather_tags': {}, 'style_tags': {}}
            
            # Process items for analytics
            categories = {}
            weather_tags = {}
            style_tags = {}
            
            formatted_items = []
            for item in items:
                # FIXED: Format item with correct column names
                formatted_item = {
                    'item_id': item['id'],  # FIXED: Use 'id' instead of 'item_id'
                    'name': item['name'],   # FIXED: Use 'name' instead of 'item_name'
                    'category': item['category'],
                    'subcategory': item.get('subcategory', ''),  # FIXED: Use 'subcategory' not 'subcategory_id'
                    'weather_tags': item.get('weather_tags', '').split(',') if item.get('weather_tags') else [],
                    'style_tags': item.get('style_tags', '').split(',') if item.get('style_tags') else [],
                    'image': item.get('image_path', '')
                }
                formatted_items.append(formatted_item)
                
                # Count categories
                category = item['category']
                categories[category] = categories.get(category, 0) + 1
                
                # Count weather tags
                if item.get('weather_tags'):
                    for tag in item['weather_tags'].split(','):
                        tag = tag.strip().lower()
                        if tag:
                            weather_tags[tag] = weather_tags.get(tag, 0) + 1
                
                # Count style tags
                if item.get('style_tags'):
                    for tag in item['style_tags'].split(','):
                        tag = tag.strip().lower()
                        if tag:
                            style_tags[tag] = style_tags.get(tag, 0) + 1
            
            return {
                'items': formatted_items,
                'categories': categories,
                'weather_tags': weather_tags,
                'style_tags': style_tags
            }
        except Exception as e:
            st.error(f"Error loading analytics: {e}")
            return {'items': [], 'categories': {}, 'weather_tags': {}, 'style_tags': {}}
    
    def get_seasonal_recommendations(self, wardrobe_data: dict, current_season: str) -> list:
        """Generate seasonal recommendations"""
        recommendations = []
        categories = wardrobe_data['categories']
        weather_tags = wardrobe_data['weather_tags']
        
        # Seasonal weather mapping
        seasonal_weather = {
            'Spring': ['mild', 'cool', 'rainy'],
            'Summer': ['hot', 'sunny', 'humid'],
            'Fall': ['cool', 'windy', 'mild'],
            'Winter': ['cold', 'freezing', 'snowy']
        }
        
        season_weather = seasonal_weather.get(current_season, ['mild'])
        
        # Check for missing seasonal items
        missing_weather_coverage = []
        for weather in season_weather:
            if weather_tags.get(weather, 0) < 2:
                missing_weather_coverage.append(weather)
        
        if missing_weather_coverage:
            recommendations.append({
                'type': 'seasonal_gap',
                'title': f'{current_season} Weather Gap',
                'message': f"Consider adding items suitable for {', '.join(missing_weather_coverage)} weather",
                'priority': 'high',
                'icon': '🌤️'
            })
        
        # Category balance for season
        if current_season == 'Summer' and categories.get('Outerwear', 0) > categories.get('Tops', 0):
            recommendations.append({
                'type': 'seasonal_balance',
                'title': 'Summer Balance',
                'message': 'Add more light tops and fewer heavy outerwear for summer',
                'priority': 'medium',
                'icon': '☀️'
            })
        
        return recommendations
    
    def get_style_recommendations(self, wardrobe_data: dict) -> list:
        """Generate style-based recommendations"""
        recommendations = []
        categories = wardrobe_data['categories']
        style_tags = wardrobe_data['style_tags']
        
        # Check for style gaps
        essential_styles = ['casual', 'formal', 'comfortable']
        missing_styles = [style for style in essential_styles if style_tags.get(style, 0) < 2]
        
        if missing_styles:
            recommendations.append({
                'type': 'style_gap',
                'title': 'Essential Styles Missing',
                'message': f"Add items for {', '.join(missing_styles)} occasions",
                'priority': 'high',
                'icon': '👗'
            })
        
        # Category balance recommendations
        total_items = sum(categories.values())
        if total_items > 0:
            tops_ratio = categories.get('Tops', 0) / total_items
            bottoms_ratio = categories.get('Bottoms', 0) / total_items
            
            if tops_ratio > 0.6:
                recommendations.append({
                    'type': 'category_balance',
                    'title': 'Too Many Tops',
                    'message': 'Consider adding more bottoms to balance your wardrobe',
                    'priority': 'medium',
                    'icon': '👖'
                })
            elif bottoms_ratio > 0.4:
                recommendations.append({
                    'type': 'category_balance',
                    'title': 'Too Many Bottoms',
                    'message': 'Consider adding more tops to balance your wardrobe',
                    'priority': 'medium',
                    'icon': '👕'
                })
        
        return recommendations
    
    def get_trending_recommendations(self, wardrobe_data: dict) -> list:
        """Generate trend-based recommendations"""
        recommendations = []
        style_tags = wardrobe_data['style_tags']
        
        # Current trend suggestions (simplified)
        trending_styles = ['minimalist', 'vintage', 'streetwear']
        missing_trends = [trend for trend in trending_styles if style_tags.get(trend, 0) == 0]
        
        if missing_trends and len(missing_trends) <= 2:  # Don't overwhelm
            recommendations.append({
                'type': 'trend',
                'title': 'Trending Styles',
                'message': f"Try adding {random.choice(missing_trends)} pieces to stay current",
                'priority': 'low',
                'icon': '👒'
            })
        
        return recommendations


# Custom CSS for recommendations
st.markdown("""
    <style>
        .recommendation-card {
            background: #faf6f1e5;
            border-radius: 1.2rem;
            padding: 1.2rem 1.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid #a26769;
            box-shadow: 0 3px 15px #dfc0a815;
        }
        .recommendation-card.high-priority {
            border-left-color: #d63384;
            background: #fef7f7;
        }
        .recommendation-card.medium-priority {
            border-left-color: #fd7e14;
            background: #fff8f5;
        }
        .recommendation-card.low-priority {
            border-left-color: #20c997;
            background: #f0fdf9;
        }
        .recommendation-header {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .recommendation-icon {
            font-size: 1.5rem;
            margin-right: 0.8rem;
        }
        .recommendation-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #4a2511;
            margin: 0;
        }
        .recommendation-message {
            color: #6c5648;
            font-size: 1rem;
            margin: 0;
            line-height: 1.4;
        }
        .recommendation-priority {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-left: auto;
        }
        .priority-high {
            background: #d631841a;
            color: #d63384;
        }
        .priority-medium {
            background: #fd7e141a;
            color: #fd7e14;
        }
        .priority-low {
            background: #20c9971a;
            color: #20c997;
        }
    </style>
""", unsafe_allow_html=True)


def get_current_season():
    """Determine current season based on date"""
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


def display_recommendation_card(recommendation):
    """Display a single recommendation card"""
    priority_class = f"{recommendation['priority']}-priority"
    
    st.markdown(f"""
        <div class="recommendation-card {priority_class}">
            <div class="recommendation-header">
                <span class="recommendation-icon">{recommendation['icon']}</span>
                <h3 class="recommendation-title">{recommendation['title']}</h3>
                <span class="recommendation-priority priority-{recommendation['priority']}">{recommendation['priority'].upper()}</span>
            </div>
            <p class="recommendation-message">{recommendation['message']}</p>
        </div>
    """, unsafe_allow_html=True)


def recommendations_page(db):
    """Main recommendations page with database parameter"""
    # Initialize database service with database connection
    global recommendations_db
    recommendations_db = RecommendationsDatabase(db)
    
    st.markdown("---")
    st.markdown("""
        <h1 style='font-size:2rem; font-weight:700; color:#4a2511; margin-bottom: 0.13em; margin-top: 0; line-height:1.05'>
        💡 Smart Recommendations
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color:#7b5155;font-size:1.08rem;'>AI-powered suggestions to enhance your wardrobe and style!</p>", unsafe_allow_html=True)
    
    username = st.session_state.username
    current_season = get_current_season()
    
    # Get wardrobe analytics
    wardrobe_data = recommendations_db.get_user_wardrobe_analytics(username)
    
    if not wardrobe_data['items']:
        st.info("📭 Add items to your wardrobe to get personalized recommendations!")
        return
    
    # Generate different types of recommendations
    seasonal_recs = recommendations_db.get_seasonal_recommendations(wardrobe_data, current_season)
    style_recs = recommendations_db.get_style_recommendations(wardrobe_data)
    trend_recs = recommendations_db.get_trending_recommendations(wardrobe_data)
    
    all_recommendations = seasonal_recs + style_recs + trend_recs
    
    if not all_recommendations:
        st.success("🌟 Your wardrobe looks well-balanced! No urgent recommendations at this time.")
        return
    
    # Sort recommendations by priority
    priority_order = {'high': 1, 'medium': 2, 'low': 3}
    all_recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
    
    # Display recommendations by category
    st.markdown(f"### 🌤️ {current_season} Recommendations")
    if seasonal_recs:
        for rec in seasonal_recs:
            display_recommendation_card(rec)
    else:
        st.info(f"You're all set for {current_season}! ✅")
    
    st.markdown("### 👗 Style Recommendations")
    if style_recs:
        for rec in style_recs:
            display_recommendation_card(rec)
    else:
        st.info("Your style coverage looks great! ✅")
    
    st.markdown("### 👒 Trending Suggestions")
    if trend_recs:
        for rec in trend_recs:
            display_recommendation_card(rec)
    else:
        st.info("You're on trend! ✅")
    
    # Summary statistics
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_items = len(wardrobe_data['items'])
        st.metric("Total Items", total_items)
    
    with col2:
        total_categories = len(wardrobe_data['categories'])
        st.metric("Categories", total_categories)
    
    with col3:
        high_priority_count = len([r for r in all_recommendations if r['priority'] == 'high'])
        st.metric("High Priority Items", high_priority_count)


# Main execution
if __name__ == "__main__":
    from config.database import get_database
    db = get_database()
    recommendations_page(db)
