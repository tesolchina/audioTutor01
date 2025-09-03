# 🧪 Testing Guide for New-Bytewise-Backend

## Quick Start Testing

### 1. **Run the Complete Test Suite**
```bash
cd /workspaces/new-bytewise-backend
python run_tests.py
```

### 2. **Run Individual Tests**
```bash
# Test server health
python run_tests.py health

# Test REST endpoints
python run_tests.py rest

# Test chat completion
python run_tests.py chat

# Test WebSocket connection
python run_tests.py websocket

# Test external API integration
python run_tests.py api

# Test audio processing
python run_tests.py audio
```

## Manual Testing Methods

### 🌐 **REST API Testing**

#### Basic Endpoints
```bash
# Test chatbot endpoint
curl http://localhost:5000/api/chatbot/a

# Test streaming avatar endpoint  
curl http://localhost:5000/api/streaming-avatar/a
```

#### Chat Completion API
```bash
curl -X POST http://localhost:5000/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "chat_history": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "api_key": "your-api-key-here",
    "model_name": "gpt-4",
    "max_tokens": 50
  }'
```

### 🔌 **WebSocket Testing**

#### Using the provided WebSocket test script:
```bash
python test_websocket.py
```

#### Using Browser DevTools:
```javascript
// Open browser console and connect to WebSocket
const socket = io('http://localhost:5000/api/streaming-avatar');

socket.on('connect', () => {
    console.log('Connected!');
    socket.emit('user_audio', 'test data');
});

socket.on('message', (data) => {
    console.log('Message received:', data);
});

socket.on('stt_result', (data) => {
    console.log('STT result:', data);
});
```

### 🤖 **External API Testing**

#### Test HKBU GenAI API integration:
```bash
python test.py
```

### 🎵 **Audio Processing Testing**

#### Test speech recognition (if you have audio files):
```python
import speech_recognition as sr
import io

# Test with the included 1.wav file (if exists)
r = sr.Recognizer()
with sr.AudioFile('1.wav') as source:
    audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        print(f"Recognized: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
```

## 📊 **Browser Testing**

### Simple HTML Test Client
Create an HTML file to test WebSocket connectivity:

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
</head>
<body>
    <h1>WebSocket Test</h1>
    <div id="output"></div>
    
    <script>
        const socket = io('http://localhost:5000/api/streaming-avatar');
        const output = document.getElementById('output');
        
        socket.on('connect', () => {
            output.innerHTML += '<p>✅ Connected to WebSocket</p>';
        });
        
        socket.on('message', (data) => {
            output.innerHTML += `<p>📨 Message: ${JSON.stringify(data)}</p>`;
        });
        
        socket.on('stt_result', (data) => {
            output.innerHTML += `<p>🎤 STT: ${JSON.stringify(data)}</p>`;
        });
        
        // Send test data after 2 seconds
        setTimeout(() => {
            socket.emit('user_audio', new Uint8Array([1,2,3,4]));
        }, 2000);
    </script>
</body>
</html>
```

## 🔍 **Performance Testing**

### Load Testing with curl:
```bash
# Test endpoint response time
time curl http://localhost:5000/api/chatbot/a

# Multiple concurrent requests
for i in {1..10}; do
    curl http://localhost:5000/api/chatbot/a &
done
wait
```

### Memory Usage Monitoring:
```bash
# Monitor server memory usage
ps aux | grep "python main.py"

# Monitor with top
top -p $(pgrep -f "python main.py")
```

## 🐛 **Debugging & Troubleshooting**

### Check Server Logs:
```bash
# If running with nohup
tail -f server.log

# If running in terminal, check console output
```

### Check Port Usage:
```bash
# See what's running on port 5000
lsof -i :5000

# Kill process on port 5000 if needed
sudo kill -9 $(lsof -t -i:5000)
```

### Test Network Connectivity:
```bash
# Test if port is accessible
telnet localhost 5000

# Test with netcat
nc -zv localhost 5000
```

## 📋 **Test Checklist**

### ✅ **Pre-deployment Testing**
- [ ] Server starts without errors
- [ ] All REST endpoints respond correctly
- [ ] WebSocket connections establish successfully
- [ ] External API integration works
- [ ] Audio processing functions correctly
- [ ] CORS headers are present
- [ ] Error handling returns proper status codes
- [ ] Memory usage is reasonable
- [ ] No memory leaks during extended operation

### ✅ **Production Readiness**
- [ ] Remove hardcoded API keys
- [ ] Configure production CORS settings
- [ ] Set up proper logging
- [ ] Configure environment variables
- [ ] Set debug=False for production
- [ ] Add rate limiting
- [ ] Add authentication if needed
- [ ] Configure HTTPS
- [ ] Set up monitoring

## 🚨 **Common Issues & Solutions**

### Server Won't Start:
- Check if port 5000 is already in use
- Verify all dependencies are installed
- Check for syntax errors in Python files

### WebSocket Connection Fails:
- Ensure SocketIO is properly configured
- Check browser CORS settings
- Verify namespace paths match

### External API Errors:
- Check API key validity
- Verify network connectivity
- Check API endpoint URLs
- Review request format

### Audio Processing Issues:
- Ensure audio files are in correct format
- Check microphone permissions (for live audio)
- Verify speech recognition API access

---

**Run the comprehensive test suite to get started:**
```bash
python run_tests.py
```
