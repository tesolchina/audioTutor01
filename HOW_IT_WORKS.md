# 📚 How Your New-Bytewise-Backend Works

## 🏗️ **Overall Architecture**

Your application is a **Flask web server** with **real-time WebSocket capabilities** that can:
- Handle HTTP API requests (REST API)
- Manage real-time connections (WebSockets)
- Process audio/speech
- Connect to external AI services

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Your Backend    │    │  External APIs  │
│                 │    │                  │    │                 │
│ • Web Interface │◄──►│ • Flask Server   │◄──►│ • HKBU GenAI    │
│ • JavaScript    │    │ • SocketIO       │    │ • Google Speech │
│ • REST calls    │    │ • Speech API     │    │ • AliCloud      │
│ • WebSocket     │    │ • Token Service  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🎯 **What Each Component Does**

### 1. **Flask Server (`main.py`)**
```python
# This is your main web server
app = Flask(__name__)                    # Creates web server
socketio = SocketIO(app)                 # Adds WebSocket support
app.run(host="0.0.0.0", port=5000)     # Runs on port 5000
```

**What it does:**
- Listens for incoming web requests on port 5000
- Serves your web interface at `http://localhost:5000`
- Routes requests to the right code (chatbot or streaming avatar)

### 2. **REST API Endpoints**
These handle traditional web requests (like when you click a button):

#### **Chatbot Router (`app/routers/chatbot.py`)**
```python
@chatbot.route("/a", methods=["GET"])           # GET /api/chatbot/a
def hello_module1():
    return {"message": "Hello from Module chatbot"}

@chatbot.route("/chat", methods=["POST"])       # POST /api/chatbot/chat  
def chat():
    # Sends your message to HKBU AI API
    # Returns AI response
```

#### **Streaming Avatar Router (`app/routers/streaming_avatar.py`)**
```python
@streaming_avatar.route("/a", methods=["GET"])  # GET /api/streaming-avatar/a
def hello_module1():
    return {"message": "Hello from Module streaming_avatar"}
```

### 3. **WebSocket (Real-time Communication)**
This handles live, instant communication:

```python
@socketio.on("connect", namespace="/api/streaming-avatar")
def handle_connect():
    # When someone connects via WebSocket
    print("Client connected!")

@socketio.on("user_audio", namespace="/api/streaming-avatar")  
def handle_user_audio(data):
    # When someone sends audio data
    # Processes speech → text using Google API
    # Sends result back instantly
```

### 4. **External API Integration**

#### **HKBU GenAI API (`test.py` shows how it works)**
```python
# Your app sends messages to HKBU's AI
url = "https://genai.hkbu.edu.hk/api/v0/rest/deployments/gpt-4.1/chat/completions"
# Gets streaming AI responses back
```

#### **Google Speech Recognition**
```python
# Converts audio → text
recognizer = sr.Recognizer()
text = recognizer.recognize_google(audio_data)
```

#### **AliCloud Token Service (`app/utils/token_service.py`)**
```python
# Generates authentication tokens for AliCloud services
token, expire_time = get_alicloud_token(access_key_id, access_key_secret)
```

## 🔄 **How Data Flows Through Your System**

### **Scenario 1: Chat Message**
```
User types message → Web Interface → POST /api/chatbot/chat → 
chatbot.py → HKBU AI API → AI Response → Back to User
```

1. User types "Hello" in web interface
2. JavaScript sends POST request to `/api/chatbot/chat`
3. `chatbot.py` receives the request
4. Formats message and sends to HKBU GenAI API
5. HKBU returns AI response
6. Your server sends response back to web interface
7. User sees AI's reply

### **Scenario 2: Audio/Speech Processing**
```
User speaks → Audio data → WebSocket → Speech Recognition → 
Text result → Back to User instantly
```

1. User connects WebSocket to `/api/streaming-avatar`
2. Sends audio data through WebSocket
3. `streaming_avatar.py` receives audio
4. Google Speech API converts audio → text
5. Result sent back through WebSocket immediately
6. User sees transcribed text

### **Scenario 3: Basic API Test**
```
User clicks button → GET /api/chatbot/a → Simple JSON response
```

1. User clicks "Test Chatbot Endpoint"
2. Browser sends GET request to `/api/chatbot/a`
3. Returns `{"message": "Hello from Module chatbot"}`

## 🌐 **Your Web Interface Explained**

The HTML file (`static/index.html`) provides a user-friendly way to test everything:

### **REST API Section**
```javascript
// When you click "Test Chatbot Endpoint"
fetch('/api/chatbot/a')           // Sends HTTP request
  .then(response => response.json())  // Gets JSON response
  .then(data => display(data))        // Shows result on page
```

### **WebSocket Section**
```javascript
// When you click "Connect WebSocket"
socket = io('/api/streaming-avatar')  // Opens live connection
socket.on('message', (data) => {      // Listens for messages
    console.log('Received:', data)     // Shows real-time updates
})
```

### **Chat Section**
```javascript
// When you click "Send Chat Message"
fetch('/api/chatbot/chat', {
    method: 'POST',
    body: JSON.stringify({
        chat_history: [your_message],
        api_key: "your-key"
    })
})
```

## 🛠️ **Key Technologies Used**

### **Backend (Python)**
- **Flask**: Web server framework
- **SocketIO**: Real-time WebSocket communication
- **SpeechRecognition**: Audio → text conversion
- **Requests**: HTTP calls to external APIs
- **CORS**: Allows web browsers to access your API

### **Frontend (JavaScript)**
- **Socket.IO**: WebSocket client
- **Fetch API**: HTTP requests
- **DOM manipulation**: Updates the web page
- **Event handling**: Button clicks, form submissions

## 💡 **What Makes This Special**

### **Real-time Capabilities**
Unlike traditional websites that require page refreshes, your app can:
- Send/receive messages instantly (WebSocket)
- Process audio in real-time
- Stream AI responses as they're generated

### **API Integration**
Your backend acts as a "bridge" between:
- Your web interface
- External AI services (HKBU)
- Speech recognition (Google)
- Cloud services (AliCloud)

### **Modular Design**
Code is organized in separate modules:
- `chatbot.py` - Chat functionality
- `streaming_avatar.py` - Real-time audio/avatar features  
- `token_service.py` - Authentication utilities
- `main.py` - Brings everything together

## 🎮 **How to Use/Test Everything**

### **1. Basic API Testing**
Click the blue buttons in your web interface:
- Tests if your server is responding
- Shows JSON responses
- Confirms endpoints are working

### **2. Chat Testing**
- Type a message in the text area
- Click "Send Chat Message"
- See how your app talks to AI services
- (Will show 401 error with test API key - that's normal!)

### **3. WebSocket Testing**
- Click "Connect WebSocket"
- Status changes to "Connected"
- Click "Send Test Audio Data"
- See real-time message exchange

### **4. Development Testing**
Use the command-line test scripts:
```bash
python run_tests.py        # Test everything
python test.py            # Test external AI API
python test_websocket.py  # Test WebSocket only
```

## 🚨 **Important Notes**

### **API Keys**
- Currently uses test/demo keys
- In production, use environment variables
- Never commit real API keys to code

### **CORS (Cross-Origin Resource Sharing)**
- Currently allows all origins (`*`)
- In production, restrict to your domain only

### **Debug Mode**
- Currently enabled for development
- Shows detailed error messages
- Turn off for production (`debug=False`)

## 🎯 **Use Cases This Backend Supports**

1. **Chatbots/AI Assistants**: Text-based AI conversations
2. **Voice Interfaces**: Speech-to-text + AI responses
3. **Real-time Communication**: Live chat, notifications
4. **Avatar/Character Systems**: Real-time audio processing for virtual characters
5. **API Gateway**: Bridge between frontend and multiple AI services

Your backend is essentially a **multi-purpose AI communication hub** that can handle both traditional web requests and real-time interactions!

Does this help clarify how everything works together? Would you like me to explain any specific part in more detail?
