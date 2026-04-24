# Quick Start Guide

## 1. Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

```bash
# Clone repository
git clone <repo-url>
cd crop-2x_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configuration

### Update .env file
```bash
# Copy environment template
cp .env .env.local

# Edit .env with your details
OPENAI_API_KEY=your-key
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
```

## 3. Run Application

```bash
# Method 1: Direct Python
python run.py

# Method 2: Using Flask
export FLASK_APP=run.py
flask run

# Method 3: Using Gunicorn (Production)
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

The app will be available at: `http://localhost:5000`

## 4. Testing the Chatbot

### Using cURL

```bash
# 1. Initialize chatbot
curl -X POST http://localhost:5000/api/chatbot/init \
  -H "Content-Type: application/json" \
  -d '{"user_type": "farmer", "device_id": "test_123"}'

# Response will include user_id, save it for next steps

# 2. Send message
curl -X POST http://localhost:5000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "message": "How can I save water?"}'

# 3. Get chat history
curl http://localhost:5000/api/chatbot/history/1?limit=10
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Initialize
init_response = requests.post(f"{BASE_URL}/chatbot/init", json={
    "user_type": "farmer"
})
user_id = init_response.json()['user_id']

# Send message
msg_response = requests.post(f"{BASE_URL}/chatbot/message", json={
    "user_id": user_id,
    "message": "What are supported crops?"
})
print(msg_response.json())
```

### Using Postman

1. Open Postman
2. Create new request
3. Set method to POST
4. URL: `http://localhost:5000/api/chatbot/init`
5. Headers: `Content-Type: application/json`
6. Body (raw JSON):
   ```json
   {
     "user_type": "farmer",
     "device_id": "postman_test"
   }
   ```
7. Click Send

## 5. Create a Lead

```bash
curl -X POST http://localhost:5000/api/leads/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "name": "Raj Kumar",
    "email": "raj@example.com",
    "phone": "+919876543210",
    "location": "Punjab",
    "lead_type": "demo_request",
    "send_whatsapp": true
  }'
```

## 6. Integrate on Website

Add this code to your website HTML:

```html
<!-- Add before closing </body> tag -->
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

<!-- Or embed directly -->
<iframe 
  src="http://localhost:5000/chatbot" 
  style="width:100%; height:600px; border:none;"
></iframe>
```

## 7. Database

### View Database

The database is stored in `crop2x.db` by default. To view:

```bash
# Using sqlite3 command line
sqlite3 crop2x.db

# View tables
.tables

# Query users
SELECT * FROM users;

# Query leads
SELECT * FROM leads;

# Exit
.exit
```

### Reset Database

```bash
# Delete database file
rm crop2x.db

# Reinitialize
python -c "from run import app; app.app_context().push(); from app import db; db.create_all()"
```

## 8. Common Issues

### Issue: Port already in use
**Solution:**
```bash
# Find process on port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Issue: Module not found
**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: Database locked
**Solution:**
```bash
# Delete lock file
rm crop2x.db-journal

# Restart app
python run.py
```

### Issue: WhatsApp not sending
**Solution:**
- Check Twilio credentials in .env
- Ensure phone numbers have country code
- In demo mode, check console logs

## 9. Environment Setup

### For Development

```bash
# Install dev dependencies
pip install pytest pytest-cov black flake8

# Run tests
pytest

# Run with coverage
pytest --cov=app

# Format code
black app/

# Lint
flake8 app/
```

### For Production

```bash
# Set environment
export FLASK_ENV=production

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --log-level info run:app

# Or use systemd service (Linux)
sudo systemctl start crop2x-backend
```

## 10. API Response Examples

### Successful Chatbot Response
```json
{
  "success": true,
  "chat_id": 1,
  "response": "🌾 Water Conservation:\n\nBased on our policies...",
  "next_action": "Lead to WhatsApp for detailed demo",
  "cta": "whatsapp",
  "policies_referenced": ["water_conservation"]
}
```

### Successful Lead Creation
```json
{
  "success": true,
  "lead_id": 1,
  "message": "Lead created successfully",
  "whatsapp_sent": true
}
```

### Error Response
```json
{
  "success": false,
  "error": "Invalid user_id"
}
```

## Support

For issues or questions:
- Check README.md for full documentation
- Review API endpoints in API_SPEC.md
- Check logs in `logs/` directory
- Contact: support@crop2x.com
