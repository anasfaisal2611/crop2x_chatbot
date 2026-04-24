# 🚀 How to Run Crop2X Backend

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- pip package manager
- Git (optional, for version control)
- Terminal/Command Prompt access

## 🏃 Quick Start (5 minutes)

### Step 1: Navigate to Project
```bash
cd c:\anas_4th_sem\projects_ncaai\crop-2x_backend
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python run.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

## 🔍 Verify Installation

Open a new terminal and test:

```bash
# Check if API is running
curl http://localhost:5000/

# Expected response:
# {
#   "message": "Crop2X Backend API",
#   "version": "1.0.0",
#   "endpoints": {...}
# }
```

## 📱 Test the Chatbot

### Using cURL

```bash
# 1. Initialize chatbot
curl -X POST http://localhost:5000/api/chatbot/init ^
  -H "Content-Type: application/json" ^
  -d "{\"user_type\": \"farmer\", \"device_id\": \"test_123\"}"

# Response:
# {
#   "success": true,
#   "user_id": 1,
#   "user_type": "farmer",
#   "message": "Chat initialized successfully"
# }

# Note the user_id (let's say it's 1)

# 2. Send a message
curl -X POST http://localhost:5000/api/chatbot/message ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\": 1, \"message\": \"How can I save water?\"}"

# Response:
# {
#   "success": true,
#   "chat_id": 1,
#   "response": "🌾 Water Conservation: ...",
#   "next_action": "Lead to WhatsApp for detailed demo",
#   "cta": "whatsapp",
#   "policies_referenced": ["water_conservation"]
# }
```

### Using Python Script

Create a file `test_chatbot.py`:

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Initialize
init_response = requests.post(f"{BASE_URL}/chatbot/init", json={
    "user_type": "farmer",
    "device_id": "python_test"
})

print("Init Response:", init_response.json())
user_id = init_response.json()['user_id']

# Send message
msg_response = requests.post(f"{BASE_URL}/chatbot/message", json={
    "user_id": user_id,
    "message": "What are supported crops?"
})

print("\nMessage Response:", msg_response.json())

# Get chat history
history_response = requests.get(f"{BASE_URL}/chatbot/history/{user_id}")
print("\nChat History:", history_response.json())
```

Run it:
```bash
python test_chatbot.py
```

## 📋 Test Lead Creation

```bash
curl -X POST http://localhost:5000/api/leads/create ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Raj Kumar\", \"email\": \"raj@example.com\", \"phone\": \"+919876543210\", \"location\": \"Punjab\", \"lead_type\": \"demo_request\", \"send_whatsapp\": false}"
```

Expected response:
```json
{
  "success": true,
  "lead_id": 1,
  "message": "Lead created successfully",
  "whatsapp_sent": false
}
```

## 📊 View Database

### Check Users
```bash
# Open SQLite
sqlite3 crop2x.db

# View users
SELECT * FROM users;

# View chats
SELECT * FROM chat_logs;

# View leads
SELECT * FROM leads;

# Exit
.exit
```

## 🌐 Access Frontend Chatbot

1. Create an HTML file `test_page.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Crop2X Test</title>
</head>
<body>
    <h1>Crop2X Chatbot Test</h1>
    
    <!-- Load chatbot -->
    <script>
        (function() {
            // Load styles
            var link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'http://localhost:5000/static/css/chatbot.css';
            document.head.appendChild(link);
            
            // Load script
            var script = document.createElement('script');
            script.src = 'http://localhost:5000/static/js/chatbot.js';
            document.body.appendChild(script);
        })();
    </script>
</body>
</html>
```

2. Open in browser: `file:///path/to/test_page.html`

## 🛑 Stop the Server

In the terminal running the app, press `Ctrl+C`

## 🚨 Troubleshooting

### "Port 5000 already in use"

```bash
# Find process on port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual ID)
taskkill /PID <PID> /F
```

### "Module not found" error

```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# Linux: source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### "Database locked" error

```bash
# Delete lock file
del crop2x.db-journal

# Delete database and restart
del crop2x.db
python run.py
```

## 📝 Common Tests

### Test 1: Farmer Journey
```bash
# 1. Init as farmer
curl -X POST http://localhost:5000/api/chatbot/init -H "Content-Type: application/json" -d "{\"user_type\": \"farmer\"}"

# Note user_id
# 2. Ask about water
curl -X POST http://localhost:5000/api/chatbot/message -H "Content-Type: application/json" -d "{\"user_id\": 1, \"message\": \"How much water can I save?\"}"

# 3. Should get WhatsApp CTA
# 4. Create lead
curl -X POST http://localhost:5000/api/leads/create -H "Content-Type: application/json" -d "{\"user_id\": 1, \"name\": \"Farmer\", \"email\": \"farmer@test.com\", \"phone\": \"+919876543210\", \"location\": \"Punjab\", \"lead_type\": \"demo_request\", \"send_whatsapp\": false}"
```

### Test 2: Partner Journey
```bash
# 1. Init as partner
curl -X POST http://localhost:5000/api/chatbot/init -H "Content-Type: application/json" -d "{\"user_type\": \"partner\"}"

# 2. Ask about partnership
curl -X POST http://localhost:5000/api/chatbot/message -H "Content-Type: application/json" -d "{\"user_id\": 2, \"message\": \"How to partner with Crop2X?\"}"

# 3. Should get partnership details
```

### Test 3: Get Statistics
```bash
curl http://localhost:5000/api/leads/stats
```

## 🔄 Development Workflow

1. **Make changes** to code files
2. **Save files** (auto-reload if DEBUG=True)
3. **Test changes** using curl or Python
4. **Check database** to verify data storage
5. **Review logs** for any errors

## 🐳 Run with Docker

```bash
# Build image
docker build -t crop2x-backend:latest .

# Run container
docker run -d -p 5000:5000 --name crop2x-api crop2x-backend:latest

# Check logs
docker logs -f crop2x-api

# Stop container
docker stop crop2x-api
```

## 📊 Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_chatbot.py::test_chatbot_init
```

## 🔐 Production Deployment

For production, see `DEPLOYMENT.md`

Quick production run:
```bash
# Set environment
set FLASK_ENV=production
set DEBUG=False

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📞 Need Help?

1. Check **README.md** for full documentation
2. Check **API_SPEC.md** for API details
3. Check **QUICKSTART.md** for quick setup
4. Check **logs/** directory for error messages
5. Check **ARCHITECTURE.md** for system design

## ✅ Checklist Before Starting

- [ ] Python 3.8+ installed
- [ ] In project directory
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured (optional for demo)
- [ ] Port 5000 is free

## 🎯 Next Steps

1. **Start the server**: `python run.py`
2. **Test endpoint**: `curl http://localhost:5000/health`
3. **Test chatbot**: Use provided cURL commands
4. **Create leads**: Submit lead data
5. **Check database**: View stored data
6. **Deploy**: Follow DEPLOYMENT.md

---

**Happy coding! 🌾**
