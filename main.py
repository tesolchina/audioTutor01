from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS  
from app.routers.streaming_avatar import streaming_avatar, register_socketio_handlers
from app.routers.chatbot import chatbot

# Create Flask app
app = Flask(__name__)

# --- Enable CORS for REST API ---
CORS(app, resources={r"/api/*": {"origins": "*"}})  

# Register blueprints
app.register_blueprint(streaming_avatar, url_prefix="/api/streaming-avatar")
app.register_blueprint(chatbot, url_prefix="/api/chatbot")

# Add a root route for the web interface
@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/avatar")
def avatar():
    return send_from_directory('static', 'avatar.html')

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory('static', filename)

# Initialize SocketIO with eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Register websocket event handlers
register_socketio_handlers(socketio)

if __name__ == "__main__":
    # Run
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)