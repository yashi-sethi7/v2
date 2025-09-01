import streamlit as st
from config.database import get_database


def authenticate_user(db, username, password):
    """Authenticate user with PyMySQL database - NO HASHING"""
    try:
        query = "SELECT user_id, username FROM users WHERE username = %s AND password = %s"
        result = db.fetch_one(query, (username, password))
        
        if result:
            return {
                'user_id': result['user_id'],
                'username': result['username']
            }
        return None
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return None


def create_user(db, username, password):
    """Create new user with PyMySQL database - NO HASHING"""
    try:
        # Check if username already exists
        check_query = "SELECT username FROM users WHERE username = %s"
        existing_user = db.fetch_one(check_query, (username,))
        
        if existing_user:
            return False, "Username already exists. Please choose a different username.", None
        
        # Insert new user with plain text password
        insert_query = "INSERT INTO users (username, password, created_at) VALUES (%s, %s, NOW())"
        user_id = db.insert_data(insert_query, (username, password))
        
        if user_id:
            return True, "Account created successfully!", user_id
        else:
            return False, "Failed to create account. Please try again.", None
            
    except Exception as e:
        return False, f"Registration error: {str(e)}", None


def validate_password(password):
    """Validate password requirements"""
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    return has_upper and has_lower and has_digit and has_special


def log_user_activity(db, user_id, activity_type, target_type, target_id):
    """Log user activity to database"""
    try:
        query = """
        INSERT INTO user_activities (user_id, activity_type, target_type, target_id, created_at) 
        VALUES (%s, %s, %s, %s, NOW())
        """
        db.insert_data(query, (user_id, activity_type, target_type, target_id))
    except Exception as e:
        # Don't break the flow if logging fails
        pass


def login_page(db):
    """Enhanced login page for V2 with basic authentication and preserved styling."""
    
    # V2 Enhancement: Back to landing button (preserved exactly)
    col_back, col_spacer = st.columns([1, 8])
    with col_back:
        if st.button("← Home", key="back_to_landing", help="Return to landing page"):
            st.session_state.show_landing = True
            st.rerun()
    
    # Preserved styling exactly as V1
    st.markdown("""
        <h1 style='text-align:center; font-size:70px; color:#A26769;'>LookBook</h1>
        <p style='text-align:center; font-size:18px; color:#7F5A5A;'>Your personal fashion planner. Stay stylish, effortlessly.</p>
        <hr style='border: 1px solid #EED6D3;'>
        <style>
            /* Gradient buttons for Login and Sign Up */
            .stButton > button {
                background: linear-gradient(90deg, #4a2511 60%, #e0c3a3 120%) !important;
                color: #fff !important;
                font-weight: 600 !important;
                border-radius: 22px !important;
                border: none !important;
                padding: 0.5em 2em !important;
                box-shadow: 0 2px 8px #bca69922;
                transition: background 0.18s;
            }
            .stButton > button:hover {
                background: linear-gradient(90deg, #7f5a5a 10%, #cbb7a6 90%) !important;
                color: #fff !important;
            }
            /* Headings in dark brown */
            .brown-heading {
                color: #4a2511 !important;
            }
            /* Lighter brown labels */
            label, .lighter-brown-label {
                color: #b19588 !important;
                font-weight: 600 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tabs[0]:
        st.markdown("<h3 class='brown-heading' style='margin-bottom: 0.6em;'>Login to your account</h3>", unsafe_allow_html=True)
        st.markdown("<style>input + label {color: #b28484 !important;}</style>", unsafe_allow_html=True)
        st.markdown("<label class='lighter-brown-label'>Username</label>", unsafe_allow_html=True)
        login_user = st.text_input("", key="login_user_login_tab", label_visibility='collapsed')
        st.markdown("<label class='lighter-brown-label'>Password</label>", unsafe_allow_html=True)
        login_pass = st.text_input("", type="password", key="login_pass_login_tab", label_visibility='collapsed')
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Login", key="login_btn_login_tab"):
                if not login_user or not login_pass:
                    st.error("Please enter both username and password.")
                else:
                    # V2 Enhancement: Basic authentication with database integration
                    user_data = authenticate_user(db, login_user, login_pass)
                    if user_data:
                        st.success(f"Welcome back, {login_user}!")
                        
                        # V2 Enhancement: Set enhanced session state
                        st.session_state.logged_in = True
                        st.session_state.username = login_user
                        st.session_state.user_id = user_data['user_id']  # New: Store user ID for V2
                        st.session_state.show_landing = False
                        
                        # V2 Enhancement: Log login activity
                        log_user_activity(
                            db=db,
                            user_id=user_data['user_id'],
                            activity_type="user_login",
                            target_type="user",
                            target_id=user_data['user_id']
                        )
                        
                        st.rerun()
                    else:
                        st.error("Incorrect username or password")
        with col2:
            st.markdown("<p style='color:#B28484;'>Forgot Password?</p>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("<h3 class='brown-heading' style='margin-bottom: 0.6em;'>Create a new account</h3>", unsafe_allow_html=True)
        st.markdown("<label class='lighter-brown-label'>Choose a username</label>", unsafe_allow_html=True)
        new_user = st.text_input("", key="new_user_signup_tab", label_visibility='collapsed')
        st.markdown("<label class='lighter-brown-label'>Choose a password</label>", unsafe_allow_html=True)
        new_pass = st.text_input("", type="password", key="new_pass_signup_tab", label_visibility='collapsed')
        st.markdown("<label class='lighter-brown-label'>Confirm password</label>", unsafe_allow_html=True)
        confirm_pass = st.text_input("", type="password", key="confirm_pass_signup_tab", label_visibility='collapsed')
        
        # V2 Enhancement: Enhanced password requirements info
        st.info("💡 Password must be at least 8 characters with uppercase, lowercase, number, and special character.")
        
        col3, col4 = st.columns([1, 1])
        with col3:
            if st.button("Sign Up", key="signup_btn_signup_tab"):
                if not new_user or not new_pass or not confirm_pass:
                    st.error("Please fill in all fields.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif not validate_password(new_pass):
                    st.error("Password must be at least 8 characters with uppercase, lowercase, number, and special character.")
                else:
                    # V2 Enhancement: Basic user creation with database integration
                    success, message, user_id = create_user(db, new_user, new_pass)
                    if success:
                        st.success("Account created successfully! Please switch to Login tab.")
                        
                        # V2 Enhancement: Log user registration activity
                        if user_id:
                            log_user_activity(
                                db=db,
                                user_id=user_id,
                                activity_type="user_registration",
                                target_type="user",
                                target_id=user_id
                            )
                    else:
                        st.error(message)
        with col4:
            st.markdown("<p style='color:#B28484;'>Already have an account?</p>", unsafe_allow_html=True)

    # Preserved footer exactly as V1
    st.markdown("""
        <hr style='border: 1px solid #EED6D3;'>
        <p style='text-align:center; font-style:italic; color:#A26769;'>"Fashion is the armor to survive the reality of everyday life." – Bill Cunningham</p>
    """, unsafe_allow_html=True)


# V2 Enhancement: Allow direct execution for testing
if __name__ == "__main__":
    # For testing purposes
    db = get_database()
    login_page(db)
