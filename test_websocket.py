#!/usr/bin/env python3
"""
Simple WebSocket client test for the streaming avatar endpoint
"""
import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connected to WebSocket server!")
    print("📤 Sending test message...")
    sio.emit('user_audio', b'test_audio_data', namespace='/api/streaming-avatar')

@sio.event
def disconnect():
    print("⚠️ Disconnected from WebSocket server")

@sio.on('message', namespace='/api/streaming-avatar')
def on_message(data):
    print(f"📨 Received message: {data}")

@sio.on('stt_result', namespace='/api/streaming-avatar')
def on_stt_result(data):
    print(f"🎤 STT Result: {data}")

def test_websocket():
    try:
        print("🔌 Connecting to WebSocket server...")
        sio.connect('http://localhost:5000', namespaces=['/api/streaming-avatar'])
        
        # Keep the connection open for a few seconds
        time.sleep(3)
        
        print("🔌 Disconnecting...")
        sio.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_websocket()
