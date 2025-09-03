from flask import Blueprint, jsonify
import io
from flask_socketio import emit, SocketIO
import numpy as np
import wave
from scipy.signal import resample
import speech_recognition as sr
import requests
import json
import base64
import os
import asyncio
from gtts import gTTS
import edge_tts
import tempfile
from pydub import AudioSegment

# ------------------------------
# Blueprint (REST endpoint)
# ------------------------------
streaming_avatar = Blueprint("streaming_avatar", __name__)

# ------------------------------
# Text-to-Speech Functions (Hong Kong Compatible)
# ------------------------------

def text_to_speech_gtts(text, lang='en'):
    """
    Google Text-to-Speech (Free, works in Hong Kong)
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Use temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            
            # Read the audio data
            with open(tmp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up
            os.unlink(tmp_file.name)
            
        return audio_data
    except Exception as e:
        print(f"GTTS Error: {e}")
        return None

async def text_to_speech_edge(text, voice='en-US-AriaNeural'):
    """
    Microsoft Edge TTS (Free, high quality, works in Hong Kong)
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        
        # Use temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            await communicate.save(tmp_file.name)
            
            # Read the audio data
            with open(tmp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up
            os.unlink(tmp_file.name)
            
        return audio_data
    except Exception as e:
        print(f"Edge TTS Error: {e}")
        return None

def get_llm_response(user_text, api_key="f78e26ce-5d62-455a-a4f6-055df1fc1a27"):
    """
    Get response from HKBU GenAI API (reusing existing logic)
    """
    try:
        url = "https://genai.hkbu.edu.hk/api/v0/rest/deployments/gpt-4.1/chat/completions?api-version=2024-12-01-preview"
        
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful educational assistant. Keep responses concise and friendly, suitable for students."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            "max_tokens": 150,
            "top_p": 1,
            "stream": False  # Non-streaming for TTS
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Sorry, I couldn't process that. Status: {response.status_code}"
            
    except Exception as e:
        print(f"LLM Error: {e}")
        return "Sorry, I'm having trouble understanding right now."


@streaming_avatar.route("/a", methods=["GET"])
def hello_module1():
    return jsonify({"message": "Hello from Module streaming_avatar"})

# ------------------------------
# WebSocket Handlers
# ------------------------------
socket_namespace = "/api/streaming-avatar"

def register_socketio_handlers(socketio: SocketIO):
    @socketio.on("connect", namespace=socket_namespace)
    def handle_connect():
        print("✅ Client connected to /streaming-avatar")
        emit("message", {"info": "Connected to WebSocket!"})

    @socketio.on("disconnect", namespace=socket_namespace)
    def handle_disconnect():
        print("⚠️ Client disconnected from /streaming-avatar")

    @socketio.on('user_audio', namespace=socket_namespace)
    def handle_user_audio(data):
        """
        SOLUTION: Handle WebM to WAV conversion for speech recognition
        """
        try:
            # Handle different data formats
            if isinstance(data, bytes):
                # Direct binary data
                audio_bytes = data
                print(f"📥 Received binary audio data, size: {len(audio_bytes)} bytes")
            elif isinstance(data, dict):
                # JSON data with base64 encoded audio
                audio_data = data.get('audio')
                if not audio_data:
                    emit('error', {'message': 'No audio data received'})
                    return
                print(f"📥 Received JSON audio data, size: {len(audio_data)} characters (base64)")
                audio_bytes = base64.b64decode(audio_data)
            elif isinstance(data, str):
                # Direct base64 string
                print(f"📥 Received string audio data, size: {len(data)} characters (base64)")
                audio_bytes = base64.b64decode(data)
            else:
                emit('error', {'message': f'Unsupported data format: {type(data)}'})
                return
            
            print(f"📦 Processing audio bytes, size: {len(audio_bytes)} bytes")
            
            # CORE SOLUTION: Convert WebM to WAV using pydub + ffmpeg
            try:
                print("🔄 Converting WebM audio to WAV format...")
                
                # Step 1: Load WebM audio with pydub (requires ffmpeg)
                audio_segment = AudioSegment.from_file(
                    io.BytesIO(audio_bytes), 
                    format="webm"
                )
                print(f"✅ WebM loaded: {len(audio_segment)}ms, {audio_segment.frame_rate}Hz, {audio_segment.channels} channels")
                
                # Step 2: Optimize for speech recognition
                # Convert to mono, 16kHz, 16-bit (ideal for speech recognition)
                audio_segment = audio_segment.set_channels(1)        # Mono
                audio_segment = audio_segment.set_frame_rate(16000)  # 16kHz
                audio_segment = audio_segment.set_sample_width(2)    # 16-bit
                
                # Step 3: Export to WAV format in memory
                wav_buffer = io.BytesIO()
                audio_segment.export(
                    wav_buffer, 
                    format="wav",
                    parameters=["-acodec", "pcm_s16le"]  # Ensure PCM encoding
                )
                wav_buffer.seek(0)
                
                print(f"✅ Converted to WAV: {len(wav_buffer.getvalue())} bytes")
                
            except Exception as conversion_error:
                print(f"❌ Audio conversion failed: {conversion_error}")
                emit('error', {'message': f'Audio format conversion failed: {conversion_error}'})
                return
            
            # Step 4: Speech recognition with converted audio
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            
            try:
                with sr.AudioFile(wav_buffer) as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    # Record the audio
                    audio_clip = recognizer.record(source)
                    
                print("🎯 Audio successfully processed by speech recognizer")
                
                # Step 5: Recognize speech
                text = recognizer.recognize_google(audio_clip, language='en-US')
                
                print(f"🗣️ User said: '{text}'")
                emit('transcription', {'text': text})
                
                # Step 6: Get LLM response
                llm_response = get_llm_response(text)
                print(f"🤖 LLM response: '{llm_response}'")
                emit('llm_response', {'text': llm_response})
                
                # Step 7: Generate TTS audio
                tts_audio = text_to_speech_gtts(llm_response)
                if tts_audio:
                    tts_base64 = base64.b64encode(tts_audio).decode('utf-8')
                    emit('tts_audio', {'audio': tts_base64})
                    print("🔊 TTS audio sent to client")
                else:
                    emit('error', {'message': 'Failed to generate TTS audio'})
                    
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                emit('error', {'message': 'Could not understand audio. Please speak clearly.'})
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                emit('error', {'message': f'Speech recognition error: {e}'})
                
        except Exception as e:
            print(f"❌ Error in handle_user_audio: {e}")
            emit('error', {'message': f'Audio processing error: {e}'})

    @socketio.on("test_tts", namespace=socket_namespace)
    def handle_test_tts(data):
        """
        Test TTS functionality directly
        """
        try:
            text = data.get("text", "Hello! This is a test of the text to speech system.")
            print(f"🔊 Testing TTS with text: {text}")
            
            # Generate TTS audio
            tts_audio = text_to_speech_gtts(text)
            if tts_audio:
                # Convert to base64 for transmission
                tts_base64 = base64.b64encode(tts_audio).decode('utf-8')
                emit('tts_audio', {'audio': tts_base64})
                emit('message', {'info': f'TTS generated for: {text}'})
            else:
                emit('error', {'message': 'Failed to generate TTS audio'})
        except Exception as e:
            print(f"Error in handle_test_tts: {e}")
            emit('error', {'message': f'TTS error: {e}'})