-- ================================
--   Version 2 - Wardrobe Project
--   Comprehensive schema.sql file
-- ================================

-- 1. users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. categories
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 3. subcategories
CREATE TABLE subcategories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 4. style_tags
CREATE TABLE style_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 5. weather_tags
CREATE TABLE weather_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 6. wardrobe_items
CREATE TABLE wardrobe_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    subcategory_id INT,
    image_path VARCHAR(500),
    color VARCHAR(50),
    brand VARCHAR(100),
    purchase_date DATE,
    price DECIMAL(10,2),
    notes TEXT,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id)
);

-- 7. outfit_items (outfit-wardrobe many-to-many)
CREATE TABLE outfit_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    outfit_id INT NOT NULL,
    wardrobe_item_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (outfit_id) REFERENCES outfits(id),
    FOREIGN KEY (wardrobe_item_id) REFERENCES wardrobe_items(id)
);

-- 8. outfits
CREATE TABLE outfits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    weather_condition VARCHAR(50),
    event_type VARCHAR(50),
    day_of_week VARCHAR(20),
    image_path VARCHAR(500),
    is_favorite TINYINT(1) DEFAULT 0,
    date_created DATE,
    last_worn DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    compatibility_score INT,
    occasion VARCHAR(100),
    season VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 9. recommendations
CREATE TABLE recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recommendation_type ENUM('outfit', 'item') NOT NULL,
    target_id INT NOT NULL,
    reason TEXT,
    weather_condition VARCHAR(50),
    event_type VARCHAR(50),
    confidence_score DECIMAL(3,2),
    is_viewed TINYINT(1) DEFAULT 0,
    is_liked TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 10. activity_logs
CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type ENUM('outfit_worn','item_added','outfit_created','recommendation_viewed','recommendation_liked','item_viewed','outfit_edited') NOT NULL,
    target_type ENUM('wardrobe_item','outfit','recommendation') NOT NULL,
    target_id INT NOT NULL,
    activity_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 11. user_activities
CREATE TABLE user_activities (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id INT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 12. outfit_style_tags
CREATE TABLE outfit_style_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    outfit_id INT NOT NULL,
    style_tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (outfit_id) REFERENCES outfits(id),
    FOREIGN KEY (style_tag_id) REFERENCES style_tags(id)
);

-- 13. outfit_weather_tags
CREATE TABLE outfit_weather_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    outfit_id INT NOT NULL,
    weather_tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (outfit_id) REFERENCES outfits(id),
    FOREIGN KEY (weather_tag_id) REFERENCES weather_tags(id)
);

-- 14. wardrobe_style_tags
CREATE TABLE wardrobe_style_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wardrobe_item_id INT NOT NULL,
    style_tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wardrobe_item_id) REFERENCES wardrobe_items(id),
    FOREIGN KEY (style_tag_id) REFERENCES style_tags(id)
);

-- 15. wardrobe_weather_tags
CREATE TABLE wardrobe_weather_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wardrobe_item_id INT NOT NULL,
    weather_tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wardrobe_item_id) REFERENCES wardrobe_items(id),
    FOREIGN KEY (weather_tag_id) REFERENCES weather_tags(id)
);
