# 📁 Complete File Guide - What Each File Does

## 🏗️ Project Structure & File Purposes

```
crop-2x_backend/
```

---

## 📄 Root Level Files

### `run.py` ⭐ **APPLICATION ENTRY POINT**
**Purpose**: Starts the entire Flask application
**What it does**:
- Creates Flask app instance
- Registers all routes (chatbot, whatsapp, leads)
- Initializes database
- Starts development server on port 5000
- Provides health check endpoint

**How to use**:
```bash
python run.py
```

**When you edit it**: Almost never - it's the main entry point

---

### `requirements.txt` 📦 **DEPENDENCY LIST**
**Purpose**: Lists all Python packages needed
**Contains**:
- Flask (web framework)
- SQLAlchemy (database ORM)
- PyPDF2 (PDF reading)
- Twilio (WhatsApp)
- CORS (cross-origin requests)
- python-dotenv (environment variables)

**How to use**:
```bash
pip install -r requirements.txt
```

**When you edit it**: When adding new Python packages

---

### `.env` 🔐 **ENVIRONMENT VARIABLES**
**Purpose**: Stores sensitive configuration
**Contains**:
- API keys (OpenAI, Twilio, etc.)
- Database URL
- Flask secret key
- WhatsApp credentials
- Email configuration

**How to use**:
```python
import os
api_key = os.getenv('OPENAI_API_KEY')
```

**When you edit it**: When setting up with real credentials

---

### `.env.example` 📋 **ENVIRONMENT TEMPLATE**
**Purpose**: Template showing all possible environment variables
**Contains**: All available configuration options with placeholders
**How to use**:
```bash
cp .env.example .env
# Then edit .env with real values
```

**When you edit it**: Almost never - it's just a template

---

### `.gitignore` 🚫 **GIT IGNORE RULES**
**Purpose**: Tells Git which files NOT to commit
**Contains**:
- `__pycache__/` - Python compiled files
- `venv/` - Virtual environment
- `.env` - Sensitive credentials
- `*.db` - Database files
- `logs/` - Log files

**When you edit it**: When adding new file types to ignore

---

### `README.md` 📖 **MAIN DOCUMENTATION**
**Purpose**: Complete project documentation
**Contains**:
- Project overview
- Installation steps
- Running instructions
- API documentation
- Database models
- Technology stack
- Deployment guides
- License and support info

**How to use**: Read first for complete understanding

---

### `QUICKSTART.md` 🚀 **QUICK SETUP GUIDE**
**Purpose**: Get up and running in 5 minutes
**Contains**:
- Prerequisites
- Installation steps
- Testing with cURL
- Common issues
- Support links

**How to use**: When you just want to get it running quickly

---

### `RUNNING_GUIDE.md` ▶️ **HOW TO RUN**
**Purpose**: Detailed steps to run the application
**Contains**:
- Virtual environment setup
- Dependency installation
- Running the app
- Testing endpoints
- Troubleshooting

**How to use**: Follow these steps to start the app

---

### `API_SPEC.md` 📡 **API SPECIFICATION**
**Purpose**: Complete REST API reference
**Contains**:
- All endpoints
- Request/response formats
- Error codes
- Authentication details
- Rate limiting info
- Examples

**How to use**: When building client apps or testing API

---

### `ARCHITECTURE.md` 🏛️ **SYSTEM DESIGN**
**Purpose**: Understand how the system works
**Contains**:
- System architecture diagram
- Module structure
- Data flow diagrams
- Database schema
- API design patterns
- Security considerations
- Performance optimization
- Technology stack

**How to use**: When you need to understand system design

---

### `DEPLOYMENT.md` 🚀 **DEPLOYMENT GUIDE**
**Purpose**: Deploy to production
**Contains**:
- Local development setup
- Docker deployment
- AWS EC2 deployment
- AWS Elastic Beanstalk
- Heroku deployment
- Production checklist
- Monitoring setup
- Troubleshooting

**How to use**: When deploying to production

---

### `PROJECT_SUMMARY.md` 📋 **PROJECT OVERVIEW**
**Purpose**: High-level project summary
**Contains**:
- Project overview
- Features implemented
- Documentation files
- Technologies used
- Quick start commands
- Current status

**How to use**: Quick reference of what's in the project

---

### `IMPLEMENTATION_CHECKLIST.md` ✅ **PROGRESS CHECKLIST**
**Purpose**: Track what's been done
**Contains**:
- Completed items (with ✅)
- Configuration steps
- Testing steps
- Deployment steps
- Customization guide
- Enhancement features
- Current limitations

**How to use**: See what's done and what's next

---

### `GETTING_STARTED.md` 🎯 **QUICK START EXAMPLES**
**Purpose**: Get started with real examples
**Contains**:
- 3-minute quick start
- Complete example journeys
- cURL command examples
- Troubleshooting
- Endpoint summary
- Success metrics

**How to use**: When you want to see working examples

---

### `Dockerfile` 🐳 **DOCKER IMAGE**
**Purpose**: Build Docker container image
**Contains**:
- Python 3.9 base image
- System dependencies
- Python dependencies installation
- Application setup
- Health check
- Port exposure
- Startup command

**How to use**:
```bash
docker build -t crop2x-backend .
docker run -p 5000:5000 crop2x-backend
```

---

### `docker-compose.yml` 🐋 **DOCKER MULTI-CONTAINER**
**Purpose**: Run full stack with Docker
**Contains**:
- Backend service (Flask)
- Database service (PostgreSQL)
- Cache service (Redis)
- Web server (Nginx)
- Volume definitions
- Network configuration

**How to use**:
```bash
docker-compose up
```

---

## 📁 `app/` Directory - Main Application

### `app/__init__.py` ⭐ **FLASK APP FACTORY**
**Purpose**: Creates and configures Flask application
**Contains**:
- Flask app creation
- Database initialization
- CORS setup
- Blueprint registration
- Database creation

**Key functions**:
- `create_app()` - Creates Flask app with config
- Database initialization
- Route registration

**When to edit**: When adding new major features or changing app structure

---

### `app/config.py` ⚙️ **CONFIGURATION MANAGEMENT**
**Purpose**: Manage different configurations
**Contains**:
- Development config (DEBUG=True)
- Testing config (in-memory DB)
- Production config (DEBUG=False)
- Shared base configuration

**When to edit**: When adding new configuration variables

---

## 📁 `app/models/` - Database Models

### `app/models/__init__.py` 💾 **DATABASE MODELS**
**Purpose**: Define database structure using SQLAlchemy
**Contains**:
- **User** model: user_type, phone, email, location, farm_size
- **ChatLog** model: stores conversations
- **Lead** model: stores customer leads
- **PolicyCache** model: stores extracted policies

**Key classes**:
```python
class User(db.Model)          # Users table
class ChatLog(db.Model)       # Chat history
class Lead(db.Model)          # Leads/contacts
class PolicyCache(db.Model)   # Policies cache
```

**When to edit**: When adding new database tables or columns

---

## 📁 `app/routes/` - API Endpoints

### `app/routes/chatbot.py` 💬 **CHATBOT API ENDPOINTS**
**Purpose**: Handle chatbot requests
**Contains**:
- `POST /chatbot/init` - Initialize chat session
- `POST /chatbot/message` - Send message to bot
- `GET /chatbot/history/<user_id>` - Get chat history
- `GET /chatbot/policies` - Get available policies

**Key functions**:
- `init_chat()` - Create/find user
- `send_message()` - Process user message and generate response
- `get_chat_history()` - Retrieve conversation history
- `get_policies()` - Retrieve policy information

**When to edit**: When adding new chatbot features

---

### `app/routes/whatsapp.py` 📱 **WHATSAPP API ENDPOINTS**
**Purpose**: Handle WhatsApp messaging
**Contains**:
- `POST /whatsapp/send` - Send message
- `POST /whatsapp/send-to-lead/<id>` - Send to specific lead
- `POST /whatsapp/webhook` - Receive incoming messages
- `POST /whatsapp/send-bulk` - Send to multiple people
- `GET /whatsapp/status/<id>` - Get message status

**When to edit**: When adding WhatsApp features

---

### `app/routes/leads.py` 👥 **LEAD MANAGEMENT ENDPOINTS**
**Purpose**: Handle lead data
**Contains**:
- `POST /leads/create` - Create new lead
- `GET /leads/list` - List all leads with filters
- `GET /leads/<id>` - Get lead details
- `PUT /leads/<id>/update-status` - Update lead status
- `GET /leads/stats` - Get statistics

**When to edit**: When modifying lead management

---

## 📁 `app/services/` - Business Logic

### `app/services/pdf_policy_scanner.py` 📄 **PDF POLICY EXTRACTION**
**Purpose**: Read and extract policies from PDF
**Contains**:
- `PDFPolicyScanner` class
- Methods to extract text from PDF
- Parse policies into categories
- Cache policies in database
- Search policies by keywords

**Key methods**:
- `extract_policies()` - Read and parse PDF
- `search_policies(query)` - Find relevant policies
- `get_cached_policies()` - Get policies from database
- `_get_dummy_policies()` - Return dummy data for testing

**When to edit**: When changing how policies are parsed

---

### `app/services/ai_response_engine.py` 🤖 **AI RESPONSE GENERATION**
**Purpose**: Generate intelligent responses based on policies
**Contains**:
- `AIResponseEngine` class
- Methods to generate responses for different user types
- Policy-based response generation
- Call-to-action determination

**Key methods**:
- `generate_response()` - Main response generation
- `_handle_farmer_query()` - Handle farmer questions
- `_handle_partner_query()` - Handle partner questions
- `_handle_enterprise_query()` - Handle enterprise questions
- `generate_whatsapp_message()` - Create WhatsApp messages

**When to edit**: When changing chatbot responses or logic

---

### `app/services/whatsapp_service.py` 📨 **WHATSAPP MESSAGING**
**Purpose**: Send WhatsApp messages via Twilio
**Contains**:
- `WhatsAppService` class
- Methods to send individual messages
- Methods to send bulk messages
- Webhook handling for incoming messages

**Key methods**:
- `send_message()` - Send to phone number
- `send_to_lead()` - Send to specific lead
- `send_admin_notification()` - Alert admins
- `handle_incoming_message()` - Process incoming messages

**When to edit**: When modifying WhatsApp behavior

---

## 📁 `app/utils/` - Utility Functions

### `app/utils/logger.py` 📝 **LOGGING**
**Purpose**: Application logging
**Contains**:
- `Logger` class
- Setup logging to file
- Methods: info(), error(), warning(), debug()

**When to edit**: When changing logging behavior

---

### `app/utils/validators.py` ✔️ **INPUT VALIDATION**
**Purpose**: Validate user input
**Contains**:
- Email validation
- Phone number validation
- User type validation
- Input sanitization
- HTML tag removal

**When to edit**: When changing validation rules

---

## 📁 `app/templates/` - HTML Templates

### `app/templates/chatbot.html` 🌐 **CHATBOT HTML**
**Purpose**: Frontend chatbot UI
**Contains**:
- Chatbot container HTML
- Message display area
- Input field
- Send button
- Lead form modal
- Minimize button

**When to edit**: When changing chatbot appearance or structure

---

## 📁 `app/static/` - Static Assets

### `app/static/css/chatbot.css` 🎨 **CHATBOT STYLING**
**Purpose**: CSS styling for chatbot widget
**Contains**:
- Container styling
- Header styling
- Message styling (bot/user)
- Input area styling
- Modal styling
- Responsive design
- Animations

**When to edit**: When changing chatbot appearance

---

### `app/static/js/chatbot.js` ⚙️ **CHATBOT JAVASCRIPT**
**Purpose**: Chatbot functionality
**Contains**:
- Initialize chatbot
- Send messages
- Display responses
- Handle CTAs (call-to-actions)
- Lead form submission
- Event handlers

**Key functions**:
- `initializeChatbot()` - Setup
- `sendMessage()` - Send to API
- `handleCTA()` - Handle actions
- `showLeadForm()` - Display form
- `submitLeadForm()` - Submit lead

**When to edit**: When changing chatbot behavior

---

## 📁 `policies/` - Policy Files

### `policies/dummy_policies.pdf` 📋 **POLICY DOCUMENT**
**Purpose**: Source document for policies
**Contains**:
- Water conservation policy
- Supported crops information
- Partnership program details
- Sustainability initiatives
- Pricing information
- Support terms

**Note**: This is a text file pretending to be PDF. Replace with real PDF when needed.

**When to edit**: When updating company policies

---

## 📁 `tests/` - Test Files

### `tests/test_chatbot.py` 🧪 **CHATBOT TESTS**
**Purpose**: Test chatbot functionality
**Contains**:
- Test initialization
- Test message sending
- Test chat history
- Test policy retrieval

**How to run**:
```bash
pytest tests/test_chatbot.py -v
```

---

### `tests/test_whatsapp.py` 🧪 **WHATSAPP TESTS**
**Purpose**: Test WhatsApp functionality
**Contains**:
- Test message sending
- Test webhook handling
- Test bulk messages

**How to run**:
```bash
pytest tests/test_whatsapp.py -v
```

---

## 🔄 How Files Work Together

```
1. Request comes in
   ↓
2. run.py → app/__init__.py
   ↓
3. Routes (app/routes/chatbot.py, etc.)
   ↓
4. Services (app/services/ai_response_engine.py, etc.)
   ↓
5. Models (app/models/__init__.py)
   ↓
6. Database (SQLAlchemy ORM)
   ↓
7. Return response as JSON
```

### Example Flow: Sending a Chat Message

```
1. Frontend (chatbot.js) sends POST /api/chatbot/message
2. chatbot.py route receives request
3. ai_response_engine.py generates response
4. pdf_policy_scanner.py extracts relevant policies
5. Models save to database
6. Response returned as JSON
7. Frontend displays message
```

---

## 📊 File Organization

```
Data Files:
  - crop2x.db (created when app runs)
  - policies/dummy_policies.pdf

Configuration:
  - .env, .env.example, requirements.txt, .gitignore

Documentation (9 files):
  - README.md, QUICKSTART.md, RUNNING_GUIDE.md, etc.

Application Code (20+ files):
  - Python (13 files in app/)
  - HTML/CSS/JS (3 files in static/)
  - Tests (2 files)

Deployment (3 files):
  - Dockerfile, docker-compose.yml, run.py
```

---

## 🎯 Quick Navigation

**Need to...**

- ✅ **Change chatbot response** → `app/services/ai_response_engine.py`
- ✅ **Add new API endpoint** → `app/routes/chatbot.py` or create new route file
- ✅ **Change database structure** → `app/models/__init__.py`
- ✅ **Change styling** → `app/static/css/chatbot.css`
- ✅ **Change chatbot behavior** → `app/static/js/chatbot.js`
- ✅ **Add configuration variable** → `.env`
- ✅ **Update documentation** → `README.md`
- ✅ **Deploy** → See `DEPLOYMENT.md`
- ✅ **Test** → Run `pytest`
- ✅ **Run app** → Execute `python run.py`

---

## 📚 Reading Order

1. **Start here**: `GETTING_STARTED.md` (quick start)
2. **Then read**: `README.md` (full docs)
3. **For API**: `API_SPEC.md` (endpoint reference)
4. **For design**: `ARCHITECTURE.md` (system design)
5. **For deployment**: `DEPLOYMENT.md` (production setup)
6. **For code**: This file (file guide)

---

## ✨ Summary

Each file has a specific purpose:
- **Entry point**: `run.py`
- **Configuration**: `.env`, `config.py`
- **API Routes**: `app/routes/*.py`
- **Business Logic**: `app/services/*.py`
- **Database**: `app/models/__init__.py`
- **Frontend**: `app/static/*.{js,css}`
- **Tests**: `tests/*.py`
- **Docs**: `*.md` files
- **Deployment**: `Dockerfile`, `docker-compose.yml`

Everything works together to create a complete, production-ready agricultural chatbot platform! 🌾

