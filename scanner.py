import os
import sqlite3
import subprocess
from rename_helper import fetch_movie_name   # Google API 获取片名

DB_PATH = "videos.db"
VIDEO_DIR = "G:/whisper"

# 分类目录
CATEGORIES = ["JXH33"]

# 需要番号替换的分类
SPECIAL_RENAME = {"河北", "其他日本", "神木丽"}

FFMPEG_PATH = "ffmpeg"

def generate_thumbnail(video_path: str, thumb_path: str):
    """生成缩略图（快速版，跳到1秒处截取1帧）"""
    try:
        if not os.path.exists(thumb_path):
            subprocess.run([
                FFMPEG_PATH,
                "-ss", "00:00:01",  # 跳到1秒
                "-i", video_path,
                "-vframes", "1",    # 截1帧
                "-q:v", "3",        # 图片质量
                thumb_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception as e:
        print(f"⚠️ 缩略图生成失败: {video_path} ({e})")

def get_display_name(filename: str, category: str) -> str:
    """生成展示名"""
    name = os.path.splitext(filename)[0]
    if category in SPECIAL_RENAME:
        try:
            new_name = fetch_movie_name(name)
            return new_name if new_name else name
        except Exception as e:
            print(f"⚠️ API 查询失败: {name} ({e})")
            return name
    return name

def scan_and_update_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 确保 videos 表有唯一约束，避免重复
    c.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filepath TEXT,
        category TEXT,
        display_name TEXT,
        thumbnail TEXT,
        play_count INTEGER DEFAULT 0,
        last_watched TIMESTAMP,
        UNIQUE(filename, category)
    )
    """)

    inserted = 0
    total_files = 0

    # 先统计总数
    for category in CATEGORIES:
        cat_path = os.path.join(VIDEO_DIR, category)
        if os.path.exists(cat_path):
            for file in os.listdir(cat_path):
                if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
                    total_files += 1

    print(f"📂 共发现 {total_files} 个视频文件，开始处理...\n")

    for category in CATEGORIES:
        cat_path = os.path.join(VIDEO_DIR, category)
        if not os.path.exists(cat_path):
            print(f"⚠️ 跳过不存在目录: {cat_path}")
            continue

        for file in os.listdir(cat_path):
            if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
                file_path = os.path.join(cat_path, file)
                filename = os.path.basename(file_path)
                display_name = get_display_name(filename, category)
                thumb_path = os.path.splitext(file_path)[0] + ".jpg"

                # 使用 INSERT OR IGNORE，避免重复
                c.execute("""
                INSERT OR IGNORE INTO videos (filename, filepath, category, display_name, thumbnail)
                VALUES (?, ?, ?, ?, ?)
                """, (filename, file_path, category, display_name, thumb_path))

                if c.rowcount > 0:  # 只有插入成功才算
                    inserted += 1
                    print(f"[{inserted}/{total_files}] {category} → {filename}")
                    generate_thumbnail(file_path, thumb_path)

    conn.commit()
    conn.close()
    print(f"\n✅ 扫描完成，本次新增 {inserted} 条记录")


if __name__ == "__main__":
    scan_and_update_db()
