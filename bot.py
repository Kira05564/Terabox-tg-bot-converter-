# bot.py
import telebot
import requests
import os
import subprocess

# 🔑 Bot Token
BOT_TOKEN = "8184133853:AAGQEC_eFSzRlVvj8qMH9G73kgujild02Tk"
bot = telebot.TeleBot(BOT_TOKEN)

# 🌐 Working Scraper API (Tested: June 2025)
SCRAPER_API = "https://teraboxsharelink.gq/api/get-download-link"

# 📦 Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Referer": "https://teraboxsharelink.gq",
    "Origin": "https://teraboxsharelink.gq",
    "Content-Type": "application/json"
}

def get_direct_link(share_url):
    try:
        # Normalize link
        if "terabox.app" in share_url:
            share_url = share_url.replace("terabox.app", "terabox.com")
        elif "terabox.com" not in share_url:
            code = share_url.split("s/")[-1].split("?")[0]
            share_url = f"https://terabox.com/s/{code}"

        print(f"🔗 Processing: {share_url}")

        payload = {"url": share_url}
        response = requests.post(SCRAPER_API, json=payload, headers=HEADERS, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data.get("direct_link") or data.get("downloadUrl")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def download_file(url, filename):
    try:
        print(f"⬇️ Downloading from: {url}")
        with requests.get(url, headers=HEADERS, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return filename if os.path.exists(filename) else None
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def convert_video(input_file, output_file):
    try:
        print("🎬 Converting video...")
        subprocess.run([
            "ffmpeg", "-i", input_file,
            "-vcodec", "libx264", "-crf", "28", "-preset", "fast",
            "-acodec", "aac", "-b:a", "128k",
            "-t", "600",  # Max 10 min (for safety)
            output_file
        ], check=True, timeout=600)
        return output_file
    except Exception as e:
        print(f"❌ FFmpeg error: {e}")
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 Terabox Video Bot\n\nSend any Terabox link. I’ll download & convert video for you! 🚀")

@bot.message_handler(func=lambda msg: "terabox" in msg.text.lower())
def handle_link(message):
    url = message.text.strip()
    bot.reply_to(message, "🔍 Extracting direct link...")

    direct_url = get_direct_link(url)
    if not direct_url:
        bot.reply_to(message, "❌ Failed to get link. Try another public link.")
        return

    bot.reply_to(message, "⬇️ Downloading video... (wait 1-5 min)")

    video_file = "video.mp4"
    if download_file(direct_url, video_file):
        bot.reply_to(message, "🎬 Converting...")

        converted_file = "converted_video.mp4"
        if convert_video(video_file, converted_file):
            bot.reply_to(message, "📤 Sending video...")
            try:
                with open(converted_file, 'rb') as v:
                    bot.send_video(message.chat.id, v, caption="✅ @YourBotNameBot")
            except Exception as e:
                bot.send_message(message.chat.id, f"📤 Send failed: {e}")
        else:
            bot.reply_to(message, "🎥 Sending original...")
            with open(video_file, 'rb') as v:
                bot.send_video(message.chat.id, v)

        # Cleanup
        os.remove(video_file)
        if os.path.exists(converted_file):
            os.remove(converted_file)
    else:
        bot.reply_to(message, "❌ Download failed. File too big or server error.")

print("🚀 Terabox Bot is LIVE on Render!")
bot.polling(none_stop=True)