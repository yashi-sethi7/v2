import streamlit as st
import streamlit.components.v1 as components


def landing_page(db=None):
    """Enhanced landing page for V2 with preserved styling and functionality."""
    
    # V2 Enhancement: Add floating elements with proper rendering
    st.markdown("""
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
    """, unsafe_allow_html=True)

    # Custom CSS - Preserved exactly with V2 enhancements
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        /* Hide Streamlit elements but keep content visible */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Hide raw HTML that appears as text */
        .stMarkdown > div > div {
            display: block !important;
        }
        
        /* Hide any element that contains raw HTML tags as text content */
        .element-container:has(.stMarkdown) .stMarkdown div:contains("<div") {
            display: none !important;
        }
        
        /* Alternative approach - hide elements containing specific HTML strings */
        div[data-testid="stMarkdownContainer"]:has(div:contains("<div class=\"features-grid\">")) {
            display: none !important;
        }
        
        /* Floating Elements */
        .floating-element {
            position: absolute;
            width: 100px;
            height: 100px;
            background: rgba(212, 165, 116, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
            z-index: 1;
        }

        .floating-element:nth-child(1) {
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }

        .floating-element:nth-child(2) {
            top: 60%;
            right: 10%;
            animation-delay: 2s;
        }

        .floating-element:nth-child(3) {
            bottom: 20%;
            left: 20%;
            animation-delay: 4s;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-20px);
            }
        }
        
        .stApp {
            font-family: 'Inter', sans-serif !important;
            background: linear-gradient(135deg, #faf8f5 0%, #f7f3f0 50%, #f0ebe5 100%) !important;
            color: #4a2511;
            overflow-x: hidden;
        }

        /* Header */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100vw;
            background: #4a2511;
            backdrop-filter: blur(20px);
            z-index: 1000;
            padding: 40px 0;
            box-shadow: 0 6px 40px rgba(74, 37, 17, 0.3);
            margin: 0;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            width: calc(100% - 40px);
            box-sizing: border-box;
        }

        .main-logo {
            font-family: 'Playfair Display', serif !important;
            font-size: 5.5rem !important;
            font-weight: 400 !important;
            color: #ffffff !important;
            margin: 0 !important;
            letter-spacing: -2px !important;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            position: relative;
            flex-shrink: 0;
        }

        .main-logo::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, rgba(212, 165, 116, 0.8), rgba(184, 149, 106, 0.8));
            border-radius: 2px;
        }

        .nav-links {
            display: flex;
            gap: 40px;
            list-style: none;
            margin: 0;
            padding: 0;
            flex-shrink: 0;
        }

        .nav-links a {
            text-decoration: none;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
            font-size: 1.2rem;
            padding: 12px 20px;
            border-radius: 25px;
            transition: all 0.3s ease;
            white-space: nowrap;
        }

        .nav-links a:hover {
            color: white;
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }

        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
            padding-top: 180px;
            padding-bottom: 20px;
        }

        .hero-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 80px;
            align-items: center;
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .hero-text h1 {
            font-family: 'Playfair Display', serif;
            font-size: 4.5rem;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 30px;
            color: #4a2511;
            letter-spacing: -2px;
        }

        .highlight {
            background: linear-gradient(135deg, #d4a574, #b8956a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-text p {
            font-size: 1.3rem;
            color: #7a5d42;
            margin-bottom: 20px;
            line-height: 1.7;
        }

        /* Significantly reduce space before buttons */
        .hero-buttons {
            margin-top: -10px;
            padding-top: 0px;
        }

        .hero-visual {
            position: relative;
            height: 600px;
        }

        .wardrobe-preview {
            position: absolute;
            width: 100%;
            height: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            transform: rotate(15deg);
        }

        .wardrobe-item {
            background: #fcf7ed;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(74, 37, 17, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }

        .wardrobe-item:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(74, 37, 17, 0.15);
        }

        .item-icon {
            font-size: 3rem;
            margin-bottom: 10px;
            color: #7a5d42;
        }

        .item-label {
            font-weight: 600;
            color: #4a2511;
            font-size: 0.9rem;
        }

        /* Features Section */
        .features {
            padding: 150px 0;
            background: rgba(255, 255, 255, 0.3);
        }

        .features h2 {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            text-align: center;
            margin-bottom: 20px;
            color: #4a2511;
            font-weight: 600;
        }

        .features-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #7a5d42;
            margin-bottom: 80px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .feature-card {
            background: rgba(252, 247, 237, 0.8);
            padding: 50px 40px;
            border-radius: 25px;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(74, 37, 17, 0.1);
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 50px rgba(74, 37, 17, 0.15);
        }

        .feature-icon {
            font-size: 4rem;
            margin-bottom: 30px;
            color: #7a5d42;
        }

        .feature-card h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            margin-bottom: 20px;
            color: #4a2511;
            font-weight: 600;
        }

        .feature-card p {
            color: #7a5d42;
            font-size: 1.1rem;
            line-height: 1.6;
        }

        /* Testimonial */
        .testimonial {
            padding: 150px 0;
            background: linear-gradient(135deg, rgba(212, 165, 116, 0.1), rgba(184, 149, 106, 0.1));
            text-align: center;
        }

        .testimonial blockquote {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-style: italic;
            color: #4a2511;
            margin-bottom: 40px;
            line-height: 1.4;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .testimonial-author {
            color: #7a5d42;
            font-size: 1.2rem;
            font-weight: 500;
        }

        /* CTA Section - Reduced vertical padding with proper spacing */
        .cta-section {
            padding: 80px 0;
            margin-top: 50px;
            text-align: center;
            background: linear-gradient(135deg, #4a2511, #7a5d42);
            color: white;
            position: relative;
            z-index: 5;
        }

        .cta-section h2 {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            margin-bottom: 30px;
            font-weight: 600;
        }

        .cta-section p {
            font-size: 1.3rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #4a2511, #7a5d42) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 18px 40px !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 35px rgba(74, 37, 17, 0.3) !important;
        }

        /* Responsive Design */
        @media (max-width: 1200px) {
            .header-content {
                max-width: 100%;
                padding: 0 15px;
            }
            
            .main-logo {
                font-size: 3.5rem !important;
            }
            
            .nav-links {
                gap: 20px;
            }
            
            .nav-links a {
                font-size: 1rem;
                padding: 8px 15px;
            }
        }
        
        @media (max-width: 768px) {
            .header {
                padding: 20px 0;
            }

            .main-logo {
                font-size: 3rem !important;
            }

            .header-content {
                flex-direction: column;
                gap: 20px;
                text-align: center;
            }
            
            .nav-links {
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .nav-links a {
                font-size: 0.9rem;
                padding: 8px 12px;
            }

            .hero {
                padding-top: 220px;
            }

            .hero-content {
                grid-template-columns: 1fr;
                text-align: center;
                gap: 40px;
            }

            .hero-text h1 {
                font-size: 3rem;
            }

            .wardrobe-preview {
                transform: rotate(0deg);
            }

            .features-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Header - Preserved exactly
    st.markdown("""
        <div class="header">
            <div class="header-content">
                <h1 class="main-logo">LookBook</h1>
                <div class="nav-links">
                    <a href="#about">About</a>
                    <a href="#contact">Contact</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Hero Section - Enhanced with V2 categories
    st.markdown("""
        <section class="hero">
            <div class="hero-content">
                <div class="hero-text">
                    <h1>Curate Your <span class="highlight">Perfect</span> Style</h1>
                    <p>Transform your wardrobe management with LookBook - the elegant solution for the modern fashion enthusiast. Organize, style, and discover your perfect look with intelligent categorization, weather-based suggestions, and AI-powered recommendations.</p>
                </div>
                <div class="hero-visual">
                    <div class="wardrobe-preview">
                        <div class="wardrobe-item">
                            <div class="item-icon">👗</div>
                            <div class="item-label">Dresses</div>
                        </div>
                        <div class="wardrobe-item">
                            <div class="item-icon">👔</div>
                            <div class="item-label">Formal</div>
                        </div>
                        <div class="wardrobe-item">
                            <div class="item-icon">👠</div>
                            <div class="item-label">Shoes</div>
                        </div>
                        <div class="wardrobe-item">
                            <div class="item-icon">👜</div>
                            <div class="item-label">Accessories</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # CTA Buttons - Enhanced with V2 navigation
    st.markdown('<div class="hero-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🚀 Start Your Journey", key="cta_primary", use_container_width=True):
            # V2 Enhancement: Clear landing state and navigate to main app
            st.session_state.show_landing = False
            st.success("🎉 Welcome to LookBook! Redirecting to your dashboard...")
            st.rerun()
        if st.button("👗 Explore Features", key="cta_secondary", use_container_width=True):
            st.success("👇 Scroll down to explore our amazing features!")
    st.markdown('</div>', unsafe_allow_html=True)

    # Features Section - Enhanced with V2 capabilities using components.html
    components.html("""
        <section class="features" id="features" style="padding: 150px 0; background: rgba(255, 255, 255, 0.3);">
            <h2 style="font-family: 'Playfair Display', serif; font-size: 3.5rem; text-align: center; margin-bottom: 20px; color: #4a2511; font-weight: 600;">Luxury Meets Functionality</h2>
            <p style="text-align: center; font-size: 1.2rem; color: #7a5d42; margin-bottom: 80px; max-width: 600px; margin-left: auto; margin-right: auto;">Experience the perfect blend of sophisticated design and powerful wardrobe management tools</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 40px; max-width: 1400px; margin: 0 auto; padding: 0 20px;">
                <div style="background: rgba(252, 247, 237, 0.8); padding: 50px 40px; border-radius: 25px; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(74, 37, 17, 0.1);">
                    <div style="font-size: 4rem; margin-bottom: 30px; color: #7a5d42;">🧥</div>
                    <h3 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 20px; color: #4a2511; font-weight: 600;">Smart Organization</h3>
                    <p style="color: #7a5d42; font-size: 1.1rem; line-height: 1.6;">Intelligently categorize your wardrobe with our advanced tagging system. Weather-appropriate and occasion-based filtering with style recommendations.</p>
                </div>
                
                <div style="background: rgba(252, 247, 237, 0.8); padding: 50px 40px; border-radius: 25px; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(74, 37, 17, 0.1);">
                    <div style="font-size: 4rem; margin-bottom: 30px; color: #7a5d42;">🤖</div>
                    <h3 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 20px; color: #4a2511; font-weight: 600;">AI Recommendations</h3>
                    <p style="color: #7a5d42; font-size: 1.1rem; line-height: 1.6;">Get personalized outfit suggestions based on weather, occasion, and your style preferences. Smart wardrobe curation at your fingertips.</p>
                </div>
                
                <div style="background: rgba(252, 247, 237, 0.8); padding: 50px 40px; border-radius: 25px; text-align: center; transition: all 0.3s ease; border: 1px solid rgba(74, 37, 17, 0.1);">
                    <div style="font-size: 4rem; margin-bottom: 30px; color: #7a5d42;">📊</div>
                    <h3 style="font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 20px; color: #4a2511; font-weight: 600;">Analytics & Insights</h3>
                    <p style="color: #7a5d42; font-size: 1.1rem; line-height: 1.6;">Track your wardrobe usage, discover style patterns, and get insights on your fashion choices. Make informed decisions about your style evolution.</p>
                </div>
            </div>
        </section>
    """, height=800)

    # All remaining sections preserved exactly as they were
    # Testimonial Section
    st.markdown("""
        <section class="testimonial">
            <div class="testimonial-content">
                <blockquote>"LookBook has transformed how I think about my wardrobe. It's not just organization – it's style curation at its finest."</blockquote>
                <div class="testimonial-author">— Fashion Enthusiast</div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # About Section
    st.markdown("""
        <section id="about" style="padding: 120px 0; background: rgba(255, 255, 255, 0.5);">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px; text-align: center;">
                <h2 style="font-family: 'Playfair Display', serif; font-size: 3.5rem; margin-bottom: 30px; color: #4a2511; font-weight: 600;">About LookBook</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; margin-top: 60px;">
                    <div style="text-align: left;">
                        <h3 style="font-family: 'Playfair Display', serif; font-size: 2rem; color: #4a2511; margin-bottom: 20px;">Our Story</h3>
                        <p style="font-size: 1.2rem; color: #7a5d42; line-height: 1.6; margin-bottom: 25px;">Born from the frustration of chaotic wardrobes and endless "I have nothing to wear" moments, LookBook was created to bring order, style, and joy back to getting dressed.</p>
                        <p style="font-size: 1.2rem; color: #7a5d42; line-height: 1.6;">We believe that fashion should be fun, organized, and accessible. Our platform combines cutting-edge technology with timeless design principles to create the ultimate wardrobe management experience.</p>
                    </div>
                    <div style="background: #fcf7ed; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(74, 37, 17, 0.1);">
                        <div style="font-size: 4rem; margin-bottom: 20px; color: #7a5d42;">💌</div>
                        <h4 style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color: #4a2511; margin-bottom: 15px;">Our Mission</h4>
                        <p style="color: #7a5d42; font-size: 1.1rem; line-height: 1.6;">To empower individuals to express their unique style with confidence, making wardrobe management an elegant and enjoyable experience.</p>
                    </div>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

    # Contact Section
    st.markdown("""
        <section id="contact" style="padding: 120px 20px 80px 20px; background: linear-gradient(135deg, rgba(212, 165, 116, 0.1), rgba(184, 149, 106, 0.1)); position: relative; z-index: 10;">
            <div style="max-width: 1000px; margin: 0 auto; text-align: center;">
                <h2 style="font-family: 'Playfair Display', serif; font-size: 3.5rem; margin-bottom: 30px; color: #4a2511; font-weight: 600;">Get In Touch</h2>
                <p style="font-size: 1.2rem; color: #7a5d42; margin-bottom: 60px; max-width: 600px; margin-left: auto; margin-right: auto;">Have questions, feedback, or just want to say hello? We'd love to hear from you!</p>
            </div>
        </section>
    """, unsafe_allow_html=True)
    
    # Contact cards - Preserved exactly
    st.markdown('<div style="max-width: 1000px; margin: -40px auto 0 auto; padding: 0 20px; position: relative; z-index: 15;">', unsafe_allow_html=True)
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")
    
    with col1:
        st.markdown("""
            <div style="background: rgba(252, 247, 237, 0.95); padding: 45px 25px; border-radius: 20px; text-align: center; box-shadow: 0 12px 35px rgba(74, 37, 17, 0.12); border: 1px solid rgba(74, 37, 17, 0.1); height: 220px; display: flex; flex-direction: column; justify-content: center; transition: all 0.3s ease; margin: 0 auto; max-width: 280px;">
                <div style="font-size: 3.5rem; margin-bottom: 20px; color: #7a5d42; line-height: 1;">📧</div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #4a2511; margin-bottom: 15px; font-weight: 600;">Email Us</h3>
                <p style="color: #7a5d42; font-size: 1rem; line-height: 1.4; margin: 0;">hello@lookbook.style</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: rgba(252, 247, 237, 0.95); padding: 45px 25px; border-radius: 20px; text-align: center; box-shadow: 0 12px 35px rgba(74, 37, 17, 0.12); border: 1px solid rgba(74, 37, 17, 0.1); height: 220px; display: flex; flex-direction: column; justify-content: center; transition: all 0.3s ease; margin: 0 auto; max-width: 280px;">
                <div style="font-size: 3.5rem; margin-bottom: 20px; color: #7a5d42; line-height: 1;">💬</div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #4a2511; margin-bottom: 15px; font-weight: 600;">Support</h3>
                <p style="color: #7a5d42; font-size: 1rem; line-height: 1.4; margin: 0;">support@lookbook.style</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: rgba(252, 247, 237, 0.95); padding: 45px 25px; border-radius: 20px; text-align: center; box-shadow: 0 12px 35px rgba(74, 37, 17, 0.12); border: 1px solid rgba(74, 37, 17, 0.1); height: 220px; display: flex; flex-direction: column; justify-content: center; transition: all 0.3s ease; margin: 0 auto; max-width: 280px;">
                <div style="font-size: 3.5rem; margin-bottom: 20px; color: #7a5d42; line-height: 1;">📣</div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #4a2511; margin-bottom: 15px; font-weight: 600;">Follow Us</h3>
                <p style="color: #7a5d42; font-size: 1rem; line-height: 1.4; margin: 0;">@lookbook_style</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
        <section class="cta-section">
            <h2>Ready to Elevate Your Style?</h2>
            <p>Join the revolution in wardrobe management and discover your signature look</p>
        </section>
    """, unsafe_allow_html=True)

    # Final CTA Button - Enhanced with V2 navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Begin Your Style Journey", key="final_cta", use_container_width=True):
            # V2 Enhancement: Clear landing state and navigate to main app
            st.session_state.show_landing = False
            st.success("☕︎ Welcome to your digital wardrobe! Let's get started...")
            st.rerun()


# V2 Enhancement: Allow direct execution for testing
if __name__ == "__main__":
    landing_page()
