import os
import telebot
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Render will inject your token securely
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- Step 1: Start Command ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    wat_button = InlineKeyboardButton("📝 Try WAT Practice", callback_data="wat_practice")
    markup.add(wat_button)
    
    bot.send_message(
        message.chat.id, 
        "Welcome, Aspirant! Ready to test your psychology?\n\nTap the button below to receive your first Word Association Test (WAT) challenge.", 
        reply_markup=markup
    )

# --- Step 2: Button Click ---
@bot.callback_query_handler(func=lambda call: call.data == "wat_practice")
def handle_wat_practice(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id, 
        "Your WAT word is: CHALLENGE\n\nType the first complete sentence that comes to your mind and send it back to me."
    )

# --- Step 3: The Upsell ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_message(
        message.chat.id,
        "✅ Sentence recorded!\n\nTo get detailed AI analysis on your psychological profile, track your progress, and access full TAT/SRT tests, download the official AI SSB app below:\n\n🔗 https://play.google.com/store/apps/details?id=com.newpromax.bookandpen29349&hl=en_IN"
    )

# --- Dummy Web Server for Render ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is running active")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Start the dummy server in the background
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    # Start the Telegram bot
    print("Bot is starting...")
    bot.infinity_polling()
