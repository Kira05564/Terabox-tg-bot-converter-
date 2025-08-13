# install_ffmpeg.py
import os
import requests

FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n4.6-latest-linux64-gpl-4.6.tar.xz"
OUTPUT_DIR = "/usr/local"

def install_ffmpeg():
    if os.path.exists("/usr/local/bin/ffmpeg"):
        print("✅ FFmpeg already installed.")
        return

    print("⏬ Downloading FFmpeg...")
    os.system("mkdir -p /tmp/ffmpeg && cd /tmp/ffmpeg")
    os.system(f"wget -O /tmp/ffmpeg/ffmpeg.tar.xz {FFMPEG_URL}")
    os.system("tar -xf /tmp/ffmpeg/ffmpeg.tar.xz -C /tmp/ffmpeg --strip-components=1")
    os.system("cp /tmp/ffmpeg/ffmpeg /usr/local/bin/")
    os.system("cp /tmp/ffmpeg/ffprobe /usr/local/bin/")
    os.system("chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe")
    print("✅ FFmpeg installed!")

if __name__ == "__main__":
    install_ffmpeg()