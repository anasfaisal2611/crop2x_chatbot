# 📖 Complete Setup & Testing Guide

## 🎯 Your Complete Crop2X Backend Project is Ready!

We've created a **complete, production-ready backend** for your agricultural chatbot platform with WhatsApp integration. Here's what you have:

### ✅ What's Included

```
✓ Full Flask Backend with REST API
✓ Database Models (Users, Chats, Leads, Policies)
✓ AI-Powered Chatbot Engine
✓ WhatsApp Integration (Twilio)
✓ PDF Policy Scanner
✓ Frontend Chatbot Widget
✓ Comprehensive Documentation
✓ Docker Setup
✓ Deployment Guides
✓ Test Suite
```

---

## 🚀 GET STARTED IN 3 MINUTES

### Step 1: Install Dependencies
```bash
cd c:\anas_4th_sem\projects_ncaai\crop-2x_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run the Server
```bash
python run.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 3: Test It Works
```bash
# In another terminal
curl http://localhost:5000/health
```

Expected response:
```json
{"status":"healthy","service":"crop2x-backend"}
```

---

## 💻 Complete Example: Farmer Journey

### 1. Initialize Chatbot
```bash
curl -X POST http://localhost:5000/api/chatbot/init ^
  -H "Content-Type: application/json" ^
  -d "{\"user_type\":\"farmer\",\"device_id\":\"farmer_123\"}"
```

**Response:**
```json
{
  "success": true,
  "user_id": 1,
  "user_type": "farmer",
  "message": "Chat initialized successfully"
}
```

### 2. Ask About Water Saving
```bash
curl -X POST http://localhost:5000/api/chatbot/message ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":1,\"message\":\"How much water can I save?\"}"
```

**Response:**
```json
{
  "success": true,
  "chat_id": 1,
  "response": "🌾 Water Conservation:\n\nBased on our policies, we help farmers reduce...",
  "next_action": "Lead to WhatsApp for detailed demo",
  "cta": "whatsapp",
  "policies_referenced": ["water_conservation"]
}
```

### 3. Submit Lead with Details
```bash
curl -X POST http://localhost:5000/api/leads/create ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\":1,\"name\":\"Rajesh Kumar\",\"email\":\"rajesh@farm.com\",\"phone\":\"+919876543210\",\"location\":\"Punjab\",\"farm_size\":\"5 acres\",\"lead_type\":\"demo_request\",\"send_whatsapp\":true}"
```

**Response:**
```json
{
  "success": true,
  "lead_id": 1,
  "message": "Lead created successfully",
  "whatsapp_sent": true
}
```

### 4. Retrieve Chat History
```bash
curl http://localhost:5000/api/chatbot/history/1?limit=10
```

**Response:**
```json
{
  "success": true,
  "count": 1,
  "history": [
    {
      "id": 1,
      "user_message": "How much water can I save?",
      "bot_response": "🌾 Water Conservation...",
      "timestamp": "2024-04-20T10:30:00"
    }
  ]
}
```

---

## 🤝 Partner Journey Example

```bash
# 1. Initialize as partner
curl -X POST http://localhost:5000/api/chatbot/init \
  -H "Content-Type: application/json" \
  -d "{\"user_type\":\"partner\"}"

# 2. Ask about partnership
curl -X POST http://localhost:5000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":2,\"message\":\"How to partner with Crop2X?\"}"

# 3. Get partnership details in response
# 4. Submit partnership inquiry as lead
curl -X POST http://localhost:5000/api/leads/create \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Company Name\",\"email\":\"contact@company.com\",\"phone\":\"+919876543210\",\"location\":\"Delhi\",\"lead_type\":\"partnership\"}"
```

---

## 📊 Get All Leads

```bash
# Get new leads only
curl "http://localhost:5000/api/leads/list?status=new"

# Get demo requests only
curl "http://localhost:5000/api/leads/list?lead_type=demo_request"

# Get with pagination
curl "http://localhost:5000/api/leads/list?page=1&limit=20"

# Get statistics
curl http://localhost:5000/api/leads/stats
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_leads": 5,
    "new": 3,
    "contacted": 1,
    "converted": 1,
    "by_type": {
      "demo_request": 3,
      "partnership": 2
    },
    "whatsapp_sent": 4
  }
}
```

---

## 🐳 Run with Docker

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop everything
docker-compose down
```

This starts:
- ✅ Backend (Flask)
- ✅ Database (PostgreSQL)
- ✅ Cache (Redis)
- ✅ Web Server (Nginx)

---

## 🧪 Run Automated Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run specific test file
pytest tests/test_chatbot.py -v

# Run with coverage report
pytest --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

---

## 📝 Frontend Chatbot Widget

To add the chatbot to your website:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Website</title>
</head>
<body>
    <h1>Welcome to Your Website</h1>
    
    <!-- Add this before </body> -->
    <script>
    (function() {
        // Load chatbot styles
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'http://localhost:5000/static/css/chatbot.css';
        document.head.appendChild(link);
        
        // Load chatbot script
        var script = document.createElement('script');
        script.src = 'http://localhost:5000/static/js/chatbot.js';
        document.body.appendChild(script);
    })();
    </script>
</body>
</html>
```

The chatbot will appear as a floating widget in the bottom-right corner.

---

## 🔧 Key Files You Need to Know About

### Backend Code
- **`run.py`** - Start the application here
- **`app/__init__.py`** - Flask app setup
- **`app/models/__init__.py`** - Database structure
- **`app/routes/chatbot.py`** - Chat API endpoints
- **`app/services/ai_response_engine.py`** - AI logic
- **`app/services/whatsapp_service.py`** - WhatsApp sending

### Configuration
- **`.env`** - Your environment variables
- **`requirements.txt`** - Python packages needed
- **`docker-compose.yml`** - Docker configuration

### Documentation
- **`README.md`** - Full documentation
- **`API_SPEC.md`** - API reference
- **`DEPLOYMENT.md`** - How to deploy

---

## 🔑 Enable Features

### To Enable WhatsApp Messages

1. Get Twilio account: https://www.twilio.com/
2. Add to `.env`:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671
```
3. Messages will now actually send via WhatsApp!

### To Enable AI Responses

1. Get OpenAI key: https://platform.openai.com/
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-your_key_here
```
3. Responses become AI-powered!

---

## 📊 Database

The system uses SQLite by default (file: `crop2x.db`)

### View Data

```bash
# Open database
sqlite3 crop2x.db

# View all tables
.tables

# View users
SELECT * FROM users;

# View leads  
SELECT * FROM leads;

# View chat history
SELECT * FROM chat_logs;

# Exit
.exit
```

### Switch to PostgreSQL

1. Install PostgreSQL
2. Create database: `createdb crop2x_db`
3. Update `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost/crop2x_db
```

---

## 🚀 Deploy to Cloud

### Option 1: AWS EC2 (Recommended)
```bash
# Full guide in DEPLOYMENT.md
# Takes ~15 minutes
# Uses Gunicorn + Nginx
```

### Option 2: Heroku (Easiest)
```bash
# Install Heroku CLI
# heroku create crop2x-backend
# git push heroku main
# Takes ~5 minutes
```

### Option 3: Docker
```bash
# docker build -t crop2x .
# docker run -p 5000:5000 crop2x
# Takes ~2 minutes
```

See `DEPLOYMENT.md` for detailed instructions for each.

---

## 🔍 Troubleshooting

### App won't start
```bash
# Check if Python is installed
python --version

# Check if port 5000 is free
netstat -ano | findstr :5000

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Get "Module not found" error
```bash
# Make sure venv is activated
# Windows: venv\Scripts\activate
# Linux: source venv/bin/activate

# Then install again
pip install -r requirements.txt
```

### Database errors
```bash
# Delete old database
del crop2x.db

# Restart app to create new one
python run.py
```

---

## 📚 Documentation Map

| Document | Purpose |
|----------|---------|
| **README.md** | Full project documentation |
| **QUICKSTART.md** | Quick setup guide |
| **RUNNING_GUIDE.md** | How to run the app |
| **API_SPEC.md** | Complete API reference |
| **ARCHITECTURE.md** | System design & architecture |
| **DEPLOYMENT.md** | How to deploy (AWS, Heroku, etc.) |
| **PROJECT_SUMMARY.md** | Project overview |
| **IMPLEMENTATION_CHECKLIST.md** | What's done & next steps |

---

## 🎓 API Endpoint Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/chatbot/init` | Start chat session |
| POST | `/api/chatbot/message` | Send message to bot |
| GET | `/api/chatbot/history/{id}` | Get chat history |
| GET | `/api/chatbot/policies` | Get available policies |
| POST | `/api/leads/create` | Create a lead |
| GET | `/api/leads/list` | List all leads |
| GET | `/api/leads/{id}` | Get lead details |
| PUT | `/api/leads/{id}/update-status` | Update lead status |
| GET | `/api/leads/stats` | Get lead statistics |
| POST | `/api/whatsapp/send` | Send WhatsApp message |
| POST | `/api/whatsapp/send-bulk` | Send bulk messages |

---

## ✨ Next Steps

### Immediate (Today)
1. [ ] Run `python run.py`
2. [ ] Test endpoint: `curl http://localhost:5000/health`
3. [ ] Try chatbot: Use cURL examples above
4. [ ] Create a test lead
5. [ ] Check database: `sqlite3 crop2x.db`

### Short Term (This Week)
1. [ ] Configure `.env` with your API keys
2. [ ] Deploy to cloud (AWS/Heroku)
3. [ ] Test WhatsApp integration
4. [ ] Integrate on your website
5. [ ] Set up monitoring/logging

### Medium Term (This Month)
1. [ ] Add user authentication
2. [ ] Create admin dashboard
3. [ ] Setup analytics
4. [ ] Add payment integration
5. [ ] Mobile app backend

### Long Term (Roadmap)
1. [ ] Multi-language support
2. [ ] Advanced ML recommendations
3. [ ] IoT device integration
4. [ ] Blockchain supply chain
5. [ ] International expansion

---

## 🎯 Success Metrics

Your backend is working correctly when:

- ✅ `python run.py` starts without errors
- ✅ `/health` endpoint responds
- ✅ Can initialize chatbot with `POST /api/chatbot/init`
- ✅ Can send message with `POST /api/chatbot/message`
- ✅ Responses include proper JSON
- ✅ Database file (`crop2x.db`) is created
- ✅ Can create leads with `POST /api/leads/create`
- ✅ Tests pass with `pytest`
- ✅ Docker setup works with `docker-compose up`

---

## 🎉 Congratulations!

Your **complete Crop2X backend** is ready to use!

### What You Have
- ✅ Working REST API
- ✅ AI-powered chatbot
- ✅ WhatsApp integration ready
- ✅ Database models
- ✅ Frontend widget
- ✅ Full documentation
- ✅ Docker deployment
- ✅ Test suite

### Start Now
```bash
cd c:\anas_4th_sem\projects_ncaai\crop-2x_backend
python run.py
```

Visit: `http://localhost:5000`

---

## 📞 Need Help?

1. **Check the docs** - See the documentation map above
2. **Review examples** - Complete cURL examples above
3. **Check logs** - Look in `logs/` directory
4. **Run tests** - `pytest` to verify everything works

---

**Happy farming with Crop2X! 🌾**
