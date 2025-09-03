# Configuration Analysis & Recommendations

## Current Configuration State

### 1. Hard-coded Configuration in `main.py`
- **Host and Port**: Server runs on `0.0.0.0:5000`
- **Debug Mode**: Set to `True`
- **CORS Settings**: Allows all origins (`"*"`) for API routes (`/api/*`)
- **SocketIO CORS**: Allows all origins (`"*"`)
- **Async Mode**: Uses `eventlet`

### 2. Hard-coded API Configuration in `test.py`
- **API URL**: `https://genai.hkbu.edu.hk/api/v0/rest/deployments/gpt-4.1/chat/completions`
- **API Key**: `f78e26ce-5d62-455a-a4f6-055df1fc1a27` ⚠️ **EXPOSED IN CODE**
- **Model Parameters**: `max_tokens=150`, `top_p=1`, `stream=True`

### 3. Hard-coded Defaults in `chatbot.py`
- **Default Model**: `gpt-4`
- **Default Max Tokens**: `150`
- **Default Top P**: `1.0`
- **API Version**: `2024-12-01-preview`

### 4. Missing Configuration Files
- **`.env` file**: Listed in `.gitignore` but doesn't exist in the workspace
- The project imports `dotenv` in `requirements.txt` but doesn't use it

## Critical Issues Identified

### Security Issues
1. **🚨 API Keys Exposed**: Sensitive API key is hardcoded in `test.py`
2. **🚨 Open CORS Policy**: Allows all origins (`"*"`) - potential security risk in production

### Configuration Management Issues
1. **No Centralized Configuration**: Settings scattered across multiple files
2. **No Environment-Specific Configs**: Same settings for all environments (dev/staging/prod)
3. **Unused Dependencies**: `dotenv` imported but not utilized

## Recommended Improvements

### Immediate Actions (High Priority)
1. **Remove exposed API key** from `test.py`
2. **Create `.env` file** for sensitive configuration
3. **Implement environment variable loading** using `dotenv`

### Configuration Structure Recommendations

#### 1. Create `.env` file
```env
# API Configuration
HKBU_API_KEY=your_api_key_here
HKBU_API_BASE_URL=https://genai.hkbu.edu.hk/api/v0/rest
API_VERSION=2024-12-01-preview

# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=True

# CORS Configuration
CORS_ORIGINS=*
SOCKETIO_CORS_ORIGINS=*

# Model Defaults
DEFAULT_MODEL=gpt-4
DEFAULT_MAX_TOKENS=150
DEFAULT_TOP_P=1.0

# AliCloud Configuration (for token_service.py)
ALICLOUD_ACCESS_KEY_ID=your_access_key_id
ALICLOUD_ACCESS_KEY_SECRET=your_access_key_secret
```

#### 2. Create `config.py` file
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    HKBU_API_KEY = os.getenv('HKBU_API_KEY')
    HKBU_API_BASE_URL = os.getenv('HKBU_API_BASE_URL', 'https://genai.hkbu.edu.hk/api/v0/rest')
    API_VERSION = os.getenv('API_VERSION', '2024-12-01-preview')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    SOCKETIO_CORS_ORIGINS = os.getenv('SOCKETIO_CORS_ORIGINS', '*')
    
    # Model Defaults
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gpt-4')
    DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS', 150))
    DEFAULT_TOP_P = float(os.getenv('DEFAULT_TOP_P', 1.0))
    
    # AliCloud Configuration
    ALICLOUD_ACCESS_KEY_ID = os.getenv('ALICLOUD_ACCESS_KEY_ID')
    ALICLOUD_ACCESS_KEY_SECRET = os.getenv('ALICLOUD_ACCESS_KEY_SECRET')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    CORS_ORIGINS = 'https://yourdomain.com'  # Restrict CORS in production

class TestingConfig(Config):
    DEBUG = True
    # Override with test-specific settings
```

#### 3. Environment-Specific Configuration Files
- `.env.development`
- `.env.production` 
- `.env.testing`

### Implementation Steps

1. **Phase 1: Security Fix**
   - [ ] Remove API key from `test.py`
   - [ ] Create `.env` file with sensitive data
   - [ ] Update `.gitignore` to ensure `.env` is excluded

2. **Phase 2: Centralized Configuration**
   - [ ] Create `config.py` with configuration classes
   - [ ] Update `main.py` to use configuration
   - [ ] Update `chatbot.py` to use configuration
   - [ ] Update `token_service.py` to use configuration

3. **Phase 3: Environment Management**
   - [ ] Create environment-specific config files
   - [ ] Add configuration validation
   - [ ] Add configuration documentation

### Security Best Practices

1. **Never commit sensitive data** to version control
2. **Use environment variables** for all sensitive configuration
3. **Validate configuration** on application startup
4. **Use different configurations** for different environments
5. **Restrict CORS origins** in production
6. **Use HTTPS** in production
7. **Implement proper authentication** for API endpoints

### Additional Recommendations

1. **Add configuration validation**: Ensure required environment variables are set
2. **Add logging configuration**: Centralize logging settings
3. **Add database configuration**: If database is added later
4. **Add monitoring configuration**: For production monitoring
5. **Add rate limiting configuration**: To prevent API abuse

## Files to Modify

1. `main.py` - Update to use centralized configuration
2. `app/routers/chatbot.py` - Remove hardcoded values
3. `app/utils/token_service.py` - Use environment variables for credentials
4. `test.py` - Remove exposed API key
5. Create `config.py` - Centralized configuration management
6. Create `.env` - Environment variables (add to .gitignore)

---

**Last Updated**: September 3, 2025  
**Status**: Recommendations - Implementation Pending
