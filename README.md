# Crop2X Backend API

## Overview

Crop2X is an AI-powered chatbot platform designed to help farmers, partners, and enterprises with agricultural solutions. The platform integrates website chatbot functionality with WhatsApp messaging for seamless communication.

## Features

### 🌾 For Farmers
- AI-powered chatbot for agricultural queries
- Water conservation optimization
- Crop management assistance
- Direct WhatsApp support connection

### 🤝 For Partners
- Partnership inquiries and information
- Revenue sharing model details
- Integration support

### 🏢 For Enterprises
- Custom solutions
- API access
- White-label options

## Project Structure

```
crop-2x_backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration settings
│   ├── models/
│   │   └── __init__.py          # Database models
│   ├── routes/
│   │   ├── chatbot.py           # Chatbot API endpoints
│   │   ├── whatsapp.py          # WhatsApp integration
│   │   └── leads.py             # Lead management
│   ├── services/
│   │   ├── pdf_policy_scanner.py  # PDF policy extraction
│   │   ├── ai_response_engine.py  # AI response generation
│   │   └── whatsapp_service.py    # WhatsApp service
│   ├── utils/
│   │   ├── logger.py            # Logging utility
│   │   └── validators.py        # Input validators
│   ├── templates/
│   │   └── chatbot.html         # Frontend HTML
│   └── static/
│       ├── css/
│       │   └── chatbot.css      # Chatbot styling
│       └── js/
│           └── chatbot.js       # Chatbot functionality
├── policies/
│   └── dummy_policies.pdf       # Policy document
├── tests/                       # Test files
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file
├── run.py                       # Application entry point
└── README.md                    # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crop-2x_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Update .env file with your configuration
   cp .env.example .env
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Configuration

Edit `.env` file with your settings:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///crop2x.db

# API Keys
OPENAI_API_KEY=your-key
GOOGLE_GENERATIVEAI_KEY=your-key

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

# Policies
POLICIES_PATH=policies/dummy_policies.pdf
```

## Running the Application

```bash
python run.py
```

The application will run at `http://localhost:5000`

### Available endpoints:

- **GET** `/` - Health check
- **GET** `/health` - Health status
- **POST** `/api/chatbot/init` - Initialize chatbot session
- **POST** `/api/chatbot/message` - Send message to chatbot
- **GET** `/api/chatbot/history/<user_id>` - Get chat history
- **GET** `/api/chatbot/policies` - Get available policies
- **POST** `/api/leads/create` - Create new lead
- **GET** `/api/leads/list` - List all leads
- **POST** `/api/whatsapp/send` - Send WhatsApp message
- **POST** `/api/whatsapp/webhook` - WhatsApp webhook receiver

## API Documentation

### Chatbot Endpoints

#### Initialize Chat
```bash
POST /api/chatbot/init
Content-Type: application/json

{
  "user_type": "farmer",
  "device_id": "device_123",
  "phone": "+919876543210"
}
```

#### Send Message
```bash
POST /api/chatbot/message
Content-Type: application/json

{
  "user_id": 1,
  "message": "How can I save water in farming?"
}
```

### Lead Management

#### Create Lead
```bash
POST /api/leads/create
Content-Type: application/json

{
  "user_id": 1,
  "name": "Raj Farmer",
  "email": "raj@example.com",
  "phone": "+919876543210",
  "location": "Punjab",
  "farm_size": "5 acres",
  "lead_type": "demo_request",
  "send_whatsapp": true
}
```

#### Get Leads
```bash
GET /api/leads/list?status=new&limit=50&page=1
```

### WhatsApp Integration

#### Send Message
```bash
POST /api/whatsapp/send
Content-Type: application/json

{
  "phone": "+919876543210",
  "message": "Hello from Crop2X!",
  "lead_id": 1
}
```

## Database Models

### User
- `id`: Primary key
- `user_type`: farmer, partner, enterprise, or general
- `phone_number`: Contact number
- `email`: Email address
- `name`: User name
- `location`: User location
- `farm_size`: Farm size (for farmers)
- `device_id`: Device identifier
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### ChatLog
- `id`: Primary key
- `user_id`: Foreign key to User
- `user_message`: User's message
- `bot_response`: Bot's response
- `response_type`: Type of response
- `policies_used`: Referenced policies
- `created_at`: Creation timestamp

### Lead
- `id`: Primary key
- `user_id`: Foreign key to User
- `name`: Lead name
- `email`: Lead email
- `phone`: Lead phone
- `location`: Location
- `farm_size`: Farm size
- `lead_type`: demo_request, partnership, general_inquiry
- `status`: new, contacted, converted, rejected
- `whatsapp_sent`: Boolean flag
- `created_at`: Creation timestamp

## Frontend Chatbot Widget

To integrate the chatbot on your website, add this to your HTML:

```html
<script>
  (function() {
    var script = document.createElement('script');
    script.src = 'http://localhost:5000/static/js/chatbot.js';
    document.head.appendChild(script);
    
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'http://localhost:5000/static/css/chatbot.css';
    document.head.appendChild(link);
  })();
</script>
```

## Testing

Run tests with:

```bash
pytest
```

## Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM
- **PyPDF2**: PDF processing
- **Twilio**: WhatsApp integration
- **OpenAI/Google AI**: AI responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary to Crop2X.

## Support

For support, contact: support@crop2x.com

## Changelog

### Version 1.0.0
- Initial release
- Chatbot functionality
- WhatsApp integration
- Lead management
- Policy-based responses
