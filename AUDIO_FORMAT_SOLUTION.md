# Audio Format Mismatch Solution

## The Problem
Browser `MediaRecorder` API outputs **WebM** format audio, but Python `SpeechRecognition` library expects **WAV/PCM** format.

## The Solution
We solve this using a **3-step conversion process**:

### Step 1: Install Dependencies
```bash
# System-level audio processing
sudo apt install -y ffmpeg

# Python audio processing libraries
pip install pydub ffmpeg-python
```

### Step 2: Audio Format Conversion Pipeline
```python
# 1. Receive WebM audio from browser
audio_bytes = base64.b64decode(audio_data)

# 2. Load WebM with pydub (requires ffmpeg)
audio_segment = AudioSegment.from_file(
    io.BytesIO(audio_bytes), 
    format="webm"
)

# 3. Optimize for speech recognition
audio_segment = audio_segment.set_channels(1)        # Mono
audio_segment = audio_segment.set_frame_rate(16000)  # 16kHz
audio_segment = audio_segment.set_sample_width(2)    # 16-bit

# 4. Export to WAV format in memory
wav_buffer = io.BytesIO()
audio_segment.export(
    wav_buffer, 
    format="wav",
    parameters=["-acodec", "pcm_s16le"]  # Ensure PCM encoding
)

# 5. Use with SpeechRecognition
with sr.AudioFile(wav_buffer) as source:
    audio_clip = recognizer.record(source)
    text = recognizer.recognize_google(audio_clip)
```

### Step 3: Complete Pipeline
```
Browser (WebM) → pydub → WAV → SpeechRecognition → Text → LLM → TTS → Audio
```

## Why This Works
1. **pydub + ffmpeg**: Handles WebM format decoding
2. **Audio optimization**: 16kHz mono optimizes speech recognition accuracy
3. **PCM encoding**: Ensures compatibility with SpeechRecognition library
4. **Memory processing**: No temporary files needed

## Key Benefits
- ✅ Handles browser MediaRecorder output directly
- ✅ Optimizes audio quality for speech recognition
- ✅ Works entirely in memory (no file I/O)
- ✅ Compatible with all major browsers
- ✅ Maintains real-time performance

## Testing
Use the `/avatar` route to test the complete voice conversation pipeline:
1. Speak into microphone
2. WebM audio automatically converted to WAV
3. Speech recognition processes audio
4. LLM generates response
5. TTS plays back response

The conversion happens transparently in the `handle_user_audio` WebSocket handler.
