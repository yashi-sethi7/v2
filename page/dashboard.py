import streamlit as st
from config.database import get_database

class DashboardAnalytics:
    """Dashboard analytics service for V2 database integration - No pandas/numpy"""
    
    def __init__(self, db):
        self.db = db
    
    def get_user_wardrobe_summary(self, user_id: int) -> dict:
        """Get wardrobe summary statistics from database"""
        try:
            # Total items count
            total_items_result = self.db.fetch_one("SELECT COUNT(*) as total_items FROM wardrobe_items WHERE user_id = %s", (user_id,))
            total_items = total_items_result['total_items'] if total_items_result else 0
            
            # Category breakdown
            categories = self.db.fetch_all("""
                SELECT category, COUNT(*) as count 
                FROM wardrobe_items 
                WHERE user_id = %s 
                GROUP BY category
            """, (user_id,))
            
            # Recent additions (last 7 days)
            recent_additions_result = self.db.fetch_one("""
                SELECT COUNT(*) as recent_additions
                FROM wardrobe_items 
                WHERE user_id = %s AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            """, (user_id,))
            recent_additions = recent_additions_result['recent_additions'] if recent_additions_result else 0
            
            return {
                'total_items': total_items,
                'categories': categories,
                'recent_additions': recent_additions
            }
        except Exception as e:
            st.error(f"Error fetching wardrobe data: {e}")
            return {'total_items': 0, 'categories': [], 'recent_additions': 0}
    
    def get_outfit_summary(self, user_id: int) -> dict:
        """Get outfit statistics from database"""
        try:
            # Total outfits
            total_outfits_result = self.db.fetch_one("SELECT COUNT(*) as total_outfits FROM outfits WHERE user_id = %s", (user_id,))
            total_outfits = total_outfits_result['total_outfits'] if total_outfits_result else 0
            
            # Recent outfits created (last 7 days)
            recent_outfits_result = self.db.fetch_one("""
                SELECT COUNT(*) as recent_outfits
                FROM outfits 
                WHERE user_id = %s AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            """, (user_id,))
            recent_outfits = recent_outfits_result['recent_outfits'] if recent_outfits_result else 0
            
            return {
                'total_outfits': total_outfits,
                'recent_outfits': recent_outfits
            }
        except Exception as e:
            st.error(f"Error fetching outfit data: {e}")
            return {'total_outfits': 0, 'recent_outfits': 0}


def dashboard_page(db):
    """Dashboard page with database parameter"""
    # Initialize analytics service with database connection
    dashboard_analytics = DashboardAnalytics(db)
    
    username = st.session_state.get("username", "User")
    
    # PRESERVED: Your exact original styling and welcome message
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #4a2511 0%, #e0c3a3 100%);
            color: #fff;
            border-radius: 1.2rem;
            padding: 2.5rem 1.8rem 2rem 1.8rem;
            margin-bottom: 2rem;
            text-align: center;
            font-family: 'Montserrat', sans-serif;
        ">
            <h2 style="
                font-weight: 700;
                font-size: 2.4rem;
                margin-bottom: 0.25em;
                letter-spacing: 0.03em;
                background: transparent !important;
            ">Welcome back, {username.title()}! ♡</h2>
            <p style="
                font-size: 1.15rem;
                font-weight: 500;
                opacity: 0.9;
                margin-top: 0;
                font-style: italic;
                background: transparent !important;
            ">Where every outfit tells your unique style story</p>
        </div>
    """, unsafe_allow_html=True)

    # PRESERVED: Your exact original navigation instruction
    st.markdown("""
        <p style="
            font-size: 1.1rem;
            color: #4a2511;
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto 2rem auto;
            font-family: 'Montserrat', sans-serif;
        ">
            Use the <strong>navigation menu</strong> above to explore your wardrobe, generate outfits, and view your saved looks with effortless elegance.
        </p>
    """, unsafe_allow_html=True)
    
    # NEW V2 ADDITION: Quick Stats Section (only if user is logged in)
    if 'user_id' in st.session_state:
        user_id = st.session_state['user_id']
        
        # Get data from database
        wardrobe_data = dashboard_analytics.get_user_wardrobe_summary(user_id)
        outfit_data = dashboard_analytics.get_outfit_summary(user_id)
        
        # Quick stats with matching brown theme
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f5f0ea 0%, #e8ddd4 100%);
                border: 2px solid #d4c4b0;
                border-radius: 1rem;
                padding: 1.5rem;
                margin: 1.5rem 0;
                font-family: 'Montserrat', sans-serif;
            ">
                <h3 style="
                    color: #4a2511;
                    text-align: center;
                    margin-bottom: 1rem;
                    font-weight: 600;
                "> ♡ Your Style Journey at a Glance ♡</h3>
        """, unsafe_allow_html=True)
        
        # Stats in columns with brown theme
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style="
                    background: #4a2511;
                    color: white;
                    padding: 1rem;
                    border-radius: 0.8rem;
                    text-align: center;
                ">
                    <h4 style="margin: 0; font-size: 1.8rem;">{wardrobe_data['total_items']}</h4>
                    <p style="margin: 0.3rem 0 0 0; opacity: 0.9;">Items</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="
                    background: #6b3e1a;
                    color: white;
                    padding: 1rem;
                    border-radius: 0.8rem;
                    text-align: center;
                ">
                    <h4 style="margin: 0; font-size: 1.8rem;">{outfit_data['total_outfits']}</h4>
                    <p style="margin: 0.3rem 0 0 0; opacity: 0.9;">Outfits</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style="
                    background: #8b5a2b;
                    color: white;
                    padding: 1rem;
                    border-radius: 0.8rem;
                    text-align: center;
                ">
                    <h4 style="margin: 0; font-size: 1.8rem;">{wardrobe_data['recent_additions']}</h4>
                    <p style="margin: 0.3rem 0 0 0; opacity: 0.9;">New Items</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style="
                    background: #a67c52;
                    color: white;
                    padding: 1rem;
                    border-radius: 0.8rem;
                    text-align: center;
                ">
                    <h4 style="margin: 0; font-size: 1.8rem;">{outfit_data['recent_outfits']}</h4>
                    <p style="margin: 0.3rem 0 0 0; opacity: 0.9;">Recent Outfits</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Close the stats container
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Category breakdown if available (using pure Streamlit)
        if wardrobe_data['categories']:
            st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #f8f5f0 0%, #ede6dc 100%);
                    border: 1px solid #d4c4b0;
                    border-radius: 0.8rem;
                    padding: 1.5rem;
                    margin-top: 1.5rem;
                    font-family: 'Montserrat', sans-serif;
                ">
                    <h4 style="
                        color: #4a2511;
                        text-align: center;
                        margin-bottom: 1rem;
                        font-weight: 700;
                        font-size: 2.0rem;
                    ">📇 Wardrobe Categories</h4>
            """, unsafe_allow_html=True)
            
            # Create category display using pure HTML/CSS (no charts)
            category_cols = st.columns(min(len(wardrobe_data['categories']), 4))
            for i, category in enumerate(wardrobe_data['categories']):
                with category_cols[i % len(category_cols)]:
                    st.markdown(f"""
                        <p style="
                            background: #4a2511;
                            color: white;
                            padding: 0.5rem;
                            border-radius: 0.5rem;
                            text-align: center;
                            margin: 0.3rem 0;
                            font-weight: 500;
                        ">
                            {category['category'].title()}: {category['count']}
                        </p>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)


# Make sure the function is available for import
if __name__ == "__main__":
    from config.database import get_database
    db = get_database()
    dashboard_page(db)
