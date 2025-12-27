
import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'database.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("Checking/Adding 'payment_method' column to 'expense' table...")
        # Check if column exists
        cursor.execute("PRAGMA table_info(expense)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'payment_method' not in columns:
            print("Column not found. Adding...")
            cursor.execute("ALTER TABLE expense ADD COLUMN payment_method TEXT DEFAULT 'Outros'")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column 'payment_method' already exists.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
