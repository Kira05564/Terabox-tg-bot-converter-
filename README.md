# 🎬 Terabox Video Converter Bot

A free & open-source Telegram bot that converts Terabox shared links into downloadable videos.  
No paid bots, no limits — just free video conversion! 🚀

![Bot Demo](https://i.imgur.com/ABC123.gif) <!-- Optional: apni video ya screenshot daal -->

---

## ✅ Features
- ✅ Terabox link → Direct video download
- ✅ Video conversion (optimized for size & quality)
- ✅ Auto FFmpeg install
- ✅ 24/7 hosting (on Render.com)
- ✅ Free & self-hosted

---

## 🚀 How to Deploy on Render.com

### 1. Fork This Repo
Click `Fork` on the top-right.

### 2. Go to [Render Dashboard](https://dashboard.render.com)
Sign in with GitHub.

### 3. Create Web Service
- Click `New +` → `Web Service`
- Connect your forked repo

### 4. Set Build & Start Commands
- **Build Command:**
  ```bash
  pip install -r requirements.txt && python install_ffmpeg.py
