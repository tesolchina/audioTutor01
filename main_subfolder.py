from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS  
import os
from app.routers.streaming_avatar import streaming_avatar, register_socketio_handlers
from app.routers.chatbot import chatbot

# Create Flask app
app = Flask(__name__)

# Get base path from environment (for subfolder deployment)
BASE_PATH = os.environ.get('BASE_PATH', '')  # e.g., '/audiotutor'

# --- Enable CORS for REST API ---
CORS(app, resources={r"/api/*": {"origins": "*"}})  

# Register blueprints with base path
app.register_blueprint(streaming_avatar, url_prefix=f"{BASE_PATH}/api/streaming-avatar")
app.register_blueprint(chatbot, url_prefix=f"{BASE_PATH}/api/chatbot")

# Add routes with base path support
@app.route(f"{BASE_PATH}/")
@app.route(f"{BASE_PATH}/index")
def index():
    return send_from_directory('static', 'index.html')

@app.route(f"{BASE_PATH}/avatar")
def avatar():
    return send_from_directory('static', 'avatar.html')

@app.route(f"{BASE_PATH}/static/<path:filename>")
def static_files(filename):
    return send_from_directory('static', filename)

# Handle root route when no base path
if not BASE_PATH:
    @app.route("/")
    def root_index():
        return send_from_directory('static', 'index.html')

# Initialize SocketIO with base path support
socket_path = f"{BASE_PATH}/socket.io/" if BASE_PATH else "/socket.io/"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet", path=socket_path)

# Register websocket event handlers
register_socketio_handlers(socketio)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    # Run
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)
