# Media Library (Qt Desktop App)

## 📌 Introduction
This is a **local media library manager** built with Qt.  
Features:  
- 🎬 **Recommended videos** (less-watched videos prioritized)  
- 🔍 **Search** (fuzzy matching by keyword)  
- 📂 **Category filtering** (Actors / Anime / MMD / Producers / Voice / JAV / Special)  
- ▶ **Playback** (PotPlayer on Windows, path display on Linux/macOS)  
- 📊 **Playback statistics** (play count + last watched timestamp)  

UI is similar to Netflix: thumbnail grid + title + play button.  

---

## 📌 Environment Setup

### Linux / macOS
```bash
sudo apt update
sudo apt install qt6-base-dev libsqlite3-dev ffmpeg
```

macOS with Homebrew:
```bash
brew install qt sqlite ffmpeg
```

### Windows
1. Install [Qt Online Installer](https://www.qt.io/download-qt-installer).  
   - Select **Qt 6.x + MinGW/MSVC** components.  
2. Install [PotPlayer](https://potplayer.daum.net/). Default path:  
   ```
   C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe
   ```
3. Install **Python 3.9+** and ensure `ffmpeg` is in PATH.  

---

## 📌 Database Setup

1. Initialize the database:
   ```bash
   python db_init.py
   ```

2. Scan video directories and generate thumbnails:
   ```bash
   python scanner.py
   ```
   - Config `VIDEO_DIR` path in `scanner.py`.  
   - Generates `videos.db` and `.jpg` thumbnails for each video.  

---

## 📌 Running the App

### With Qt Creator
1. Open the project (`main.cpp`, `mainwindow.*`).  
2. Build & Run.  

### Command Line
Linux/macOS:
```bash
g++ main.cpp mainwindow.cpp -o media-library     `pkg-config --cflags --libs Qt6Widgets Qt6Sql` -lsqlite3
./media-library
```

Windows (MinGW):
```bash
g++ main.cpp mainwindow.cpp -o media-library.exe     -IC:\Qt\6.x.x\mingw_64\include -LC:\Qt\6.x.x\mingw_64\lib     -lsqlite3 -lQt6Widgets -lQt6Sql
media-library.exe
```
