import sqlite3

DB_PATH = "videos.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filepath TEXT,
        category TEXT,
        display_name TEXT,
        thumbnail TEXT,
        play_count INTEGER DEFAULT 0,
        last_watched TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")

if __name__ == "__main__":
    init_db()
