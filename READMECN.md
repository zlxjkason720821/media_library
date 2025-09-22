# 媒体库（Qt 桌面应用）

## 📌 项目介绍
这是一个 **本地媒体库管理应用**（Qt 实现），功能包括：  
- 🎬 **推荐视频**（优先展示播放次数少的影片）  
- 🔍 **搜索功能**（输入关键字模糊搜索）  
- 📂 **分类切换**（Actors / Anime / MMD / Producers / Voice / JAV / Special）  
- ▶ **播放功能**（Windows 调用 PotPlayer，Linux/macOS 输出路径）  
- 📊 **播放统计**（自动更新播放次数与最近播放时间）  

界面类似 Netflix：缩略图网格 + 标题 + 播放按钮。  

---

## 📌 环境准备

### Linux / macOS
```bash
sudo apt update
sudo apt install qt6-base-dev libsqlite3-dev ffmpeg
```
(macOS 使用 Homebrew)  
```bash
brew install qt sqlite ffmpeg
```

### Windows
1. 安装 [Qt 官方在线安装器](https://www.qt.io/download-qt-installer)。  
   - 选择 **Qt 6.x + MinGW 或 MSVC** 组件。  
2. 安装 [PotPlayer](https://potplayer.daum.net/)，默认路径：  
   ```
   C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe
   ```
3. 确保已安装 **Python 3.9+**，并且已添加 `ffmpeg` 到系统 PATH。  

---

## 📌 数据库构建

1. 初始化数据库  
   ```bash
   python db_init.py
   ```

2. 扫描视频目录并生成缩略图  
   ```bash
   python scanner.py
   ```
   - 在 `scanner.py` 中修改 `VIDEO_DIR` 路径  
   - 自动生成 `videos.db` 和视频缩略图  

---

## 📌 运行应用

### Qt Creator 运行
1. 打开 `main.cpp / mainwindow.*`。  
2. 点击编译并运行。  

### 命令行运行
Linux/macOS:  
```bash
g++ main.cpp mainwindow.cpp -o media-library     `pkg-config --cflags --libs Qt6Widgets Qt6Sql` -lsqlite3
./media-library
```

Windows（MinGW）：  
```bash
g++ main.cpp mainwindow.cpp -o media-library.exe     -IC:\Qt\6.x.x\mingw_64\include -LC:\Qt\6.x.x\mingw_64\lib     -lsqlite3 -lQt6Widgets -lQt6Sql
media-library.exe
```
