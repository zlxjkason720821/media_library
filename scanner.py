import os
import sqlite3
import subprocess

DB_PATH = "videos.db"
VIDEO_DIR = "/mnt/media/Videos"  # ⚠️ Mac/Linux 路径, Windows 用 "D:/Videos"
CATEGORIES = ["Actors", "Anime", "MMD", "Producers", "Voice", "JAV", "Special"]

def generate_thumbnail(video_path: str, thumb_path: str):
    if not os.path.exists(thumb_path):
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vf", "select=eq(n\\,0)",
            "-q:v", "3", thumb_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def scan_and_update_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for category in CATEGORIES:
        cat_path = os.path.join(VIDEO_DIR, category)
        if not os.path.exists(cat_path):
            continue

        for file in os.listdir(cat_path):
            if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
                file_path = os.path.join(cat_path, file)
                filename = os.path.basename(file_path)
                display_name = os.path.splitext(filename)[0]

                thumb_path = os.path.splitext(file_path)[0] + ".jpg"
                generate_thumbnail(file_path, thumb_path)

                c.execute("""
                INSERT INTO videos (filename, filepath, category, display_name, thumbnail)
                VALUES (?, ?, ?, ?, ?)
                """, (filename, file_path, category, display_name, thumb_path))

    conn.commit()
    conn.close()
    print("✅ 扫描完成，缩略图已生成并写入数据库")

if __name__ == "__main__":
    scan_and_update_db()