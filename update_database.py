import sqlite3
import os

def update_database():
    db_path = 'carshowroom.db'
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Create a backup of the old table
        cursor.execute("ALTER TABLE user RENAME TO user_old")
        
        # 2. Create new table with correct schema
        cursor.execute("""
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 3. Copy data from old table to new table
        # Check what columns exist in old table
        cursor.execute("PRAGMA table_info(user_old)")
        old_columns = [col[1] for col in cursor.fetchall()]
        
        if 'email' in old_columns:
            # If email already exists, copy all data
            cursor.execute("""
            INSERT INTO user (id, username, email, password, is_admin, created_at)
            SELECT id, username, email, password, is_admin, created_at
            FROM user_old
            """)
        else:
            # If email doesn't exist, add placeholder email
            cursor.execute("""
            INSERT INTO user (id, username, email, password, is_admin, created_at)
            SELECT id, username, username || '@example.com', password, is_admin, created_at
            FROM user_old
            """)
        
        # 4. Update the admin email specifically
        cursor.execute("""
        UPDATE user 
        SET email = 'admin@carshowroom.com'
        WHERE username = 'admin'
        """)
        
        # 5. Drop the old table
        cursor.execute("DROP TABLE user_old")
        
        # 6. Update Car table if needed
        cursor.execute("PRAGMA table_info(car)")
        car_columns = [col[1] for col in cursor.fetchall()]
        
        if 'available' not in car_columns:
            cursor.execute("ALTER TABLE car ADD COLUMN available BOOLEAN DEFAULT TRUE")
        
        conn.commit()
        print("Database updated successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()