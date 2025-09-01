import streamlit as st
from streamlit_option_menu import option_menu
from config.settings import PAGE_CONFIG
from config.database import get_database
import pymysql  # RESTORED - needed for database connection check
from page import login, dashboard, wardrobe, generator, saved_outfits, analytics
from page.landing import landing_page


# ==== GLOBAL CONFIGURATION ====
st.set_page_config(**PAGE_CONFIG)


# Initialize database connection
db = get_database()


# ==== GLOBAL STYLE (PRESERVED EXACTLY) ====
st.markdown("""
    <style>
        /* Hide the Streamlit header and menu */
        .stApp > header {
            background-color: transparent;
        }
        
        /* Hide the Streamlit menu button */
        .stApp > div[data-testid="stDecoration"] {
            display: none;
        }
        
        /* Hide the "Made with Streamlit" footer */
        .stApp > footer {
            display: none;
        }
        
        /* Hide the main menu */
        #MainMenu {
            display: none;
        }
        
        /* Hide the Streamlit header */
        header[data-testid="stHeader"] {
            display: none;
        }
        
        /* Hide the fork ribbon */
        .stActionButton {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
        html, body {
            background-color: #f7f6f3 !important;
            font-family: 'Montserrat', 'Segoe UI', sans-serif;
        }
        [class*="st-"] {
            font-family: 'Montserrat', 'Segoe UI', sans-serif;
        }
        .big-heading {
            font-size: 2.3rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            margin-bottom: 0.3em;
        }
        .hr-custom {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, #e0c3a3 30%, #faf6f1 100%);
            margin: 0.7em 0 1.2em 0;
        }
        button[kind="primary"] {
            border-radius: 1.5em !important;
            background: linear-gradient(90deg, #4a2511 60%, #e0c3a3 120%);
            color: #fff;
            font-weight: 600;
            border: none;
            padding: 0.5em 1.6em;
            margin-left: 0.7em;
            box-shadow: 0 2px 8px #9d87692e;
            transition: background 0.2s;
        }
        button[kind="primary"]:hover {
            background: linear-gradient(90deg, #6b401e 20%, #dcbd96 100%);
        }
        .nav-container {
            box-shadow: 0 4px 16px #e5ccb458;
            border-radius: 16px;
            margin-bottom: 1em;
            background: #f5ede2;
        }
        .welcome-user {
            font-size: 1.2rem;
            font-weight: 400;
            color: #4a2511;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .profile-avatar {
            background: #e0c3a3;
            color: #fff;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.7em;
            margin-right: 10px;
        }
        .stApp, .block-container, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
            background: none !important;
            background-color: transparent !important;
        }
    </style>
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


# ==== SESSION STATE DEFAULTS ====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "editing_item" not in st.session_state:
    st.session_state.editing_item = None
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True
if "selected_categories" not in st.session_state:
    st.session_state.selected_categories = []
if "selected_weather_tags" not in st.session_state:
    st.session_state.selected_weather_tags = []
if "selected_style_tags" not in st.session_state:
    st.session_state.selected_style_tags = []


def logout():
    """Enhanced logout with activity logging for V2."""
    global db
    try:
        from services.analytics_service import log_user_activity

        if st.session_state.get("user_id"):
            log_user_activity(
                db=db,
                user_id=st.session_state.user_id,
                activity_type="user_logout",
                target_type="user",
                target_id=st.session_state.user_id
            )
    except ImportError:
        pass

    # Clear session and logout
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.session_state.show_landing = True
    st.success("Logged out successfully!")
    st.rerun()


def main():
    # Database connection check
    try:
        if not db.connection or not db.connection.open:
            st.error("❌ Database connection failed. Please check your settings.")
            st.stop()
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        st.stop()

    if st.session_state.show_landing and not st.session_state.logged_in:
        landing_page()
    elif not st.session_state.logged_in:
        login.login_page(db)
    else:
        with st.container():
            st.markdown('<div class="nav-container">', unsafe_allow_html=True)

            menu_options = ["Dashboard", "Wardrobe", "Outfits", "Fit Generator", "Saved Outfits", "Recommendations", "Analytics"]
            menu_icons = ["house", "bag", "layers", "palette", "bookmark", "robot", "bar-chart"]

            current_page = st.session_state.get('current_page', "Dashboard")

            selected = option_menu(
                menu_title=None,
                options=menu_options,
                icons=menu_icons,
                menu_icon="cast",
                default_index=menu_options.index(current_page) if current_page in menu_options else 0,
                orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "rgba(0,0,0,0)"},
                    "icon": {"color": "#9a6e3a", "font-size": "22px"},
                    "nav-link": {
                        "font-size": "18px",
                        "font-weight": "600",
                        "text-align": "center",
                        "margin": "0px 10px",
                        "color": "#52331d",
                        "opacity": "0.92",
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(90deg, #e0c3a3 30%, #4a2511 100%)",
                        "color": "#fff",
                        "border-radius": "12px",
                        "box-shadow": "0 2px 8px #c1a48124",
                    },
                },
            )

            if selected != current_page:
                st.session_state.current_page = selected
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            col_left, col_right = st.columns([8, 1.4])
            with col_left:
                st.markdown(
                    f"""
                    <div class="welcome-user" style="font-size:2.0em;>
                        <span class="profile-avatar" style="font-size:2.0em;">👤</span>
                        Welcome, <strong>{st.session_state.username} ♡</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_right:
                st.button("Logout", key="logout", help="Sign out and return to login", use_container_width=True, on_click=logout)

            st.markdown('<hr class="hr-custom">', unsafe_allow_html=True)

            if selected == "Dashboard":
                dashboard.dashboard_page(db)
            elif selected == "Wardrobe":
                wardrobe.wardrobe_page(db)
            elif selected == "Outfits":
                try:
                    from page import outfits
                    outfits.outfits_page(db)
                except ImportError:
                    st.error("Outfits page not implemented yet.")
            elif selected == "Fit Generator":
                generator.generator_page(db)
            elif selected == "Saved Outfits":
                saved_outfits.saved_outfits_page(db)
            elif selected == "Recommendations":
                try:
                    from page import recommendations
                    recommendations.recommendations_page(db)
                except ImportError:
                    st.error("Recommendations page not implemented yet.")
            elif selected == "Analytics":
                analytics.analytics_page(db)


if __name__ == "__main__":
    main()

