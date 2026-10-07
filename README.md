# SOCIAL - Video Downloader
**Developed by Thiago**

SOCIAL is a lightweight, terminal-based video downloader that supports major social platforms. It automatically detects the platform, extracts the video ID, and saves content to an organized folder structure.

### Supported Platforms
- YouTube (including Shorts, Embed, Live)
- TikTok
- Instagram (Posts, Reels, TV)
- Facebook (including fb.watch and shared links)
- X / Twitter

### Key Features
- Automatic platform detection and ID extraction
- Quality selection: Best, 1080p, 720p, 480p, 360p, Audio Only (MP3)
- Single and batch download mode
- Organized storage per platform
- Progress bar with download speed and ETA
- Safe filename handling for Android
- Built-in dependency checker for Termux

### Installation

**For Termux (Recommended):**
```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg nodejs -y
pip install -r requirements.txt
python social.py
