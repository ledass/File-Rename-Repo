import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from bot import bot  # Imports your Pyrogram client

# Koyeb injects a PORT environment variable, default to 8000
PORT = int(os.environ.get("PORT", 8000))

# --- KOYEB HEALTH CHECK SERVER ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Respond with 200 OK to satisfy Koyeb's health checks
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is healthy and running!")
        
    # Disable logging for every health check request to avoid console spam
    def log_message(self, format, *args):
        pass

def run_health_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
    print(f"✅ Health check server listening on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    # 1. Start the HTTP server in a background thread
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # 2. Start the Pyrogram bot
    print("🚀 Starting Pyrogram bot...")
    bot.run()
