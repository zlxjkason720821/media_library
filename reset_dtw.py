import os
import sqlite3
import subprocess

DB_PATH = "videos.db"
VIDEO_DIR = "G:/whisper/DTW"
FFMPEG_PATH = "ffmpeg"

def generate_thumbnail(video_path: str, thumb_path: str):
    """生成缩略图"""
    try:
        if not os.path.exists(thumb_path):
            subprocess.run([
                FFMPEG_PATH,
                "-ss", "00:00:01",
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "3",
                thumb_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"✅ 缩略图生成: {thumb_path}")
    except Exception as e:
        print(f"⚠️ 缩略图失败: {video_path} ({e})")

def reset_dtw():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. 删除数据库里所有 DTW 分类的视频
    c.execute("DELETE FROM videos WHERE category='DTW'")
    conn.commit()
    print("🗑️ 已清空数据库中的 DTW 分类")

    # 2. 遍历 DTW 文件夹，重新插入
    inserted = 0
    for file in os.listdir(VIDEO_DIR):
        if file.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
            filepath = os.path.join(VIDEO_DIR, file)
            filename = os.path.basename(filepath)
            display_name = os.path.splitext(filename)[0]  # 用清理过的文件名
            thumb_path = filepath + ".thumb.jpg"

            # 生成缩略图
            generate_thumbnail(filepath, thumb_path)

            # 插入数据库
            c.execute("""
                INSERT INTO videos (filename, filepath, category, display_name, thumbnail, play_count)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (filename, filepath, "DTW", display_name, thumb_path))
            inserted += 1

    conn.commit()
    conn.close()
    print(f"🎉 已重新插入 {inserted} 条 DTW 视频")

if __name__ == "__main__":
    reset_dtw()
