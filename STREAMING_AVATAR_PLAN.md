# 🎭 Building Your Streaming Avatar System

## 🎯 **Your Vision: Interactive Learning Avatar**

```
Student speaks → Microphone → Speech-to-Text → LLM → Text Response → Text-to-Speech → Avatar speaks back
```

## ✅ **What You Already Have (80% Complete!)**

### **1. Backend Infrastructure ✅**
- ✅ Flask server with WebSocket support
- ✅ Real-time communication via SocketIO
- ✅ Speech recognition (Google Speech API)
- ✅ LLM integration (HKBU GenAI API)
- ✅ CORS setup for web browsers
- ✅ Modular architecture

### **2. Core Components Working ✅**
- ✅ **Speech-to-Text**: `streaming_avatar.py` already handles audio input
- ✅ **LLM API**: `chatbot.py` already sends/receives from AI
- ✅ **Real-time Communication**: WebSocket infrastructure ready
- ✅ **Web Interface**: Browser-based testing interface

## 🔧 **What Needs to Be Added**

### **1. Text-to-Speech (TTS) 🎤**
Convert LLM text responses back to audio

### **2. Audio Streaming 📡**
Stream audio back to the client efficiently

### **3. Frontend Avatar Interface 👤**
Visual avatar that appears to speak

### **4. Integration Pipeline 🔄**
Connect all pieces in a smooth workflow

## 🚀 **Implementation Plan**

### **Phase 1: Add Text-to-Speech to Backend**

#### **Option A: Google Text-to-Speech (Recommended)**
```python
# Add to requirements.txt
google-cloud-texttospeech

# Add to streaming_avatar.py
from google.cloud import texttospeech

def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return response.audio_content
```

#### **Option B: Microsoft Azure Speech (Alternative)**
```python
# Add to requirements.txt
azure-cognitiveservices-speech

# Implementation
import azure.cognitiveservices.speech as speechsdk
```

#### **Option C: OpenAI TTS (Modern Option)**
```python
# Add to requirements.txt
openai

# Implementation
from openai import OpenAI
client = OpenAI()

def text_to_speech(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    return response.content
```

### **Phase 2: Update Backend for Complete Pipeline**

#### **Enhanced `streaming_avatar.py`**
```python
@socketio.on("user_audio", namespace=socket_namespace)
def handle_user_audio(data):
    try:
        # 1. Speech to Text (Already implemented ✅)
        text = speech_to_text(data)
        emit("stt_result", {"text": text})
        
        # 2. Send to LLM for response
        llm_response = get_llm_response(text)
        emit("llm_response", {"text": llm_response})
        
        # 3. Convert response to speech (NEW)
        audio_data = text_to_speech(llm_response)
        emit("avatar_speech", {"audio": audio_data})
        
    except Exception as e:
        emit("error", {"message": str(e)})

def get_llm_response(user_text):
    # Use existing chatbot logic
    chat_history = [
        {"role": "system", "content": "You are a helpful educational assistant."},
        {"role": "user", "content": user_text}
    ]
    # Call HKBU API (reuse existing code from chatbot.py)
    response = chat_completion(chat_history, api_key, model_name)
    return response["choices"][0]["message"]["content"]
```

### **Phase 3: Enhanced Frontend with Avatar**

#### **Create Avatar Interface (`static/avatar.html`)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Streaming Avatar - Educational Assistant</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
</head>
<body>
    <div class="avatar-container">
        <div class="avatar-face" id="avatarFace">
            <div class="eyes"></div>
            <div class="mouth" id="avatarMouth"></div>
        </div>
        
        <div class="controls">
            <button id="startListening">🎤 Start Talking</button>
            <button id="stopListening">⏹️ Stop</button>
        </div>
        
        <div class="conversation">
            <div id="transcript"></div>
            <div id="response"></div>
        </div>
        
        <audio id="avatarAudio" autoplay></audio>
    </div>

    <script>
        const socket = io('/api/streaming-avatar');
        let mediaRecorder;
        let isRecording = false;

        // Start audio recording
        document.getElementById('startListening').onclick = async () => {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    // Send audio to backend
                    socket.emit('user_audio', event.data);
                }
            };
            
            mediaRecorder.start(1000); // Send audio every second
            isRecording = true;
        };

        // Handle responses from backend
        socket.on('stt_result', (data) => {
            document.getElementById('transcript').innerText = 'You said: ' + data.text;
        });

        socket.on('llm_response', (data) => {
            document.getElementById('response').innerText = 'Avatar: ' + data.text;
            animateAvatarSpeaking(); // Visual feedback
        });

        socket.on('avatar_speech', (data) => {
            // Play audio response
            const audio = document.getElementById('avatarAudio');
            const blob = new Blob([data.audio], { type: 'audio/mp3' });
            audio.src = URL.createObjectURL(blob);
            audio.play();
        });

        function animateAvatarSpeaking() {
            // Simple mouth animation
            const mouth = document.getElementById('avatarMouth');
            mouth.style.transform = 'scaleY(1.5)';
            setTimeout(() => {
                mouth.style.transform = 'scaleY(1)';
            }, 500);
        }
    </script>

    <style>
        .avatar-container {
            text-align: center;
            padding: 20px;
        }
        
        .avatar-face {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            margin: 0 auto 20px;
            position: relative;
        }
        
        .eyes {
            position: absolute;
            top: 60px;
            left: 50px;
            width: 100px;
            height: 20px;
            background: white;
            border-radius: 50%;
        }
        
        .eyes::before, .eyes::after {
            content: '';
            position: absolute;
            width: 15px;
            height: 15px;
            background: black;
            border-radius: 50%;
            top: 2.5px;
        }
        
        .eyes::before { left: 20px; }
        .eyes::after { right: 20px; }
        
        .mouth {
            position: absolute;
            bottom: 50px;
            left: 75px;
            width: 50px;
            height: 10px;
            background: #333;
            border-radius: 25px;
            transition: transform 0.3s;
        }
        
        .controls {
            margin: 20px 0;
        }
        
        .controls button {
            padding: 15px 30px;
            font-size: 16px;
            margin: 0 10px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
        }
        
        .conversation {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
    </style>
</body>
</html>
```

### **Phase 4: Advanced Features**

#### **1. Voice Activity Detection**
```javascript
// Automatically start/stop recording based on voice
const audioContext = new AudioContext();
const analyser = audioContext.createAnalyser();
// Detect when user starts/stops speaking
```

#### **2. Avatar Lip Sync**
```javascript
// Sync avatar mouth movements with speech
function syncLipMovement(audioData) {
    // Analyze audio frequency and animate mouth accordingly
}
```

#### **3. Educational Context**
```python
# Enhanced system prompt for educational scenarios
EDUCATIONAL_PROMPT = """
You are an AI teaching assistant. You help students learn by:
- Asking engaging questions
- Providing clear explanations
- Encouraging curiosity
- Adapting to the student's level
Be friendly, patient, and encouraging.
"""
```

## 📋 **Step-by-Step Implementation**

### **Immediate Next Steps (This Week)**

1. **Add Text-to-Speech Service**
   ```bash
   pip install google-cloud-texttospeech
   # OR
   pip install openai  # for OpenAI TTS
   ```

2. **Update `streaming_avatar.py`**
   - Add TTS function
   - Connect STT → LLM → TTS pipeline
   - Test with existing web interface

3. **Test Complete Pipeline**
   ```bash
   python run_tests.py
   # Then test in browser
   ```

### **Short-term (Next 2 Weeks)**

4. **Create Dedicated Avatar Interface**
   - Build `static/avatar.html`
   - Add microphone access
   - Implement audio playback

5. **Add Visual Avatar**
   - Simple animated face
   - Mouth movements during speech
   - Visual feedback for listening/speaking states

### **Medium-term (Next Month)**

6. **Enhanced Features**
   - Voice activity detection
   - Better lip synchronization
   - Educational conversation context
   - Multiple avatar personalities

7. **Production Preparation**
   - Secure API key management
   - Performance optimization
   - Error handling improvements

## 🤔 **Do You Need a Separate Project?**

**No! Your current backend is perfect for this.** You just need to:

1. **Add TTS capability** (1-2 days)
2. **Enhance the frontend** (3-5 days)
3. **Connect the pipeline** (1-2 days)

Your existing architecture with Flask + SocketIO is ideal for real-time avatar interactions.

## 🎯 **Which Approach Would You Like to Take?**

1. **🚀 Quick Start**: Add basic TTS to existing backend first
2. **🎨 Visual First**: Build avatar interface then add TTS
3. **🔄 Pipeline**: Focus on complete STT → LLM → TTS flow

Would you like me to start implementing any of these phases? I can help you add the TTS functionality to your existing backend right now!
