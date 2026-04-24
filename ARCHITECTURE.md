# Architecture & Design Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Website)                      │
│                    Chatbot Widget (JS)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Nginx (Load Balancer)                       │
│              SSL/TLS Termination                            │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │Gunicorn 1│    │Gunicorn 2│    │Gunicorn N│
  │  Worker  │    │  Worker  │    │  Worker  │
  └──────┬───┘    └──────┬───┘    └──────┬───┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
              ┌────────────────────────┐
              │   Flask Application    │
              │  ├─ Routes             │
              │  ├─ Services           │
              │  └─ Models             │
              └──────────┬─────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      ┌────────┐   ┌──────────┐   ┌──────────┐
      │SQLAlch │   │PDF Parser│   │Twilio API│
      │emy ORM │   │          │   │(WhatsApp)│
      └───┬────┘   └────┬─────┘   └────┬─────┘
          │             │              │
          ▼             ▼              ▼
      ┌─────────────────────────────────────┐
      │      External Services              │
      │  ├─ PostgreSQL DB                   │
      │  ├─ Redis Cache                     │
      │  ├─ OpenAI/Google AI API            │
      │  └─ Twilio WhatsApp                 │
      └─────────────────────────────────────┘
```

## Module Architecture

```
app/
├── models/
│   ├── User              # User information
│   ├── ChatLog           # Conversation history
│   ├── Lead              # Lead/contact information
│   └── PolicyCache       # Cached policies
│
├── routes/
│   ├── chatbot.py        # Chat endpoints
│   ├── whatsapp.py       # WhatsApp webhooks
│   └── leads.py          # Lead management
│
├── services/
│   ├── pdf_policy_scanner    # Extract policies from PDF
│   ├── ai_response_engine    # Generate AI responses
│   └── whatsapp_service      # Send WhatsApp messages
│
├── utils/
│   ├── logger.py         # Logging
│   └── validators.py     # Input validation
│
└── static/
    ├── css/
    │   └── chatbot.css   # Chatbot styling
    └── js/
        └── chatbot.js    # Chatbot functionality
```

## Data Flow

### Chatbot Message Flow
```
1. User sends message from website
   └─> POST /api/chatbot/message
       │
       ├─> Validate user & message
       │
       ├─> Pass to AIResponseEngine
       │   ├─> Extract relevant policies
       │   ├─> Generate contextual response
       │   └─> Determine call-to-action
       │
       ├─> Store conversation in ChatLog
       │
       └─> Return response with CTA

2. Based on CTA:
   - "whatsapp" → Show WhatsApp connect button
   - "lead_form" → Display lead form
   - "none" → Continue chat
```

### Lead Capture Flow
```
1. User submits lead form
   └─> POST /api/leads/create
       │
       ├─> Validate lead data
       │
       ├─> Store in database
       │
       ├─> Generate AI welcome message
       │
       └─> Send via WhatsApp (optional)
           ├─> Format message
           ├─> Call Twilio API
           └─> Store message ID
```

### WhatsApp Integration Flow
```
1. Backend generates message
   └─> whatsapp_service.send_message()
       │
       ├─> Format phone number
       │
       ├─> Call Twilio API
       │   └─> Create message
       │
       ├─> Receive message SID
       │
       └─> Store in database

2. Incoming WhatsApp message
   └─> POST /api/whatsapp/webhook
       │
       ├─> Verify webhook signature
       │
       ├─> Extract sender & message
       │
       ├─> Store in ChatLog
       │
       └─> Process & respond
           └─> Generate reply via AI
           └─> Send back via WhatsApp
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user_type VARCHAR(50),
    phone_number VARCHAR(20) UNIQUE,
    email VARCHAR(120) UNIQUE,
    name VARCHAR(120),
    location VARCHAR(200),
    farm_size VARCHAR(100),
    device_id VARCHAR(200) UNIQUE,
    created_at DATETIME,
    updated_at DATETIME
);
```

### ChatLogs Table
```sql
CREATE TABLE chat_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    user_message TEXT,
    bot_response TEXT,
    response_type VARCHAR(50),
    policies_used JSON,
    created_at DATETIME
);
```

### Leads Table
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    name VARCHAR(120),
    email VARCHAR(120),
    phone VARCHAR(20),
    location VARCHAR(200),
    farm_size VARCHAR(100),
    lead_type VARCHAR(50),
    message TEXT,
    status VARCHAR(50),
    whatsapp_sent BOOLEAN,
    whatsapp_message_id VARCHAR(200),
    created_at DATETIME,
    updated_at DATETIME
);
```

### PolicyCache Table
```sql
CREATE TABLE policy_cache (
    id INTEGER PRIMARY KEY,
    category VARCHAR(100),
    policy_text TEXT,
    keywords JSON,
    last_updated DATETIME
);
```

## API Design Patterns

### Request/Response Format
```json
{
  "success": true/false,
  "data": {...},
  "error": "Error message if applicable",
  "timestamp": "2024-04-20T10:30:00Z"
}
```

### Error Handling
- 400: Bad Request (validation failed)
- 404: Not Found (resource doesn't exist)
- 500: Server Error (internal error)
- All errors return JSON with error message

### Pagination
- Default: 50 items per page
- Max: 1000 items per page
- Parameters: `?page=1&limit=50`

## Security Considerations

1. **Input Validation**
   - All user inputs are validated
   - Malicious HTML/scripts removed
   - Phone numbers verified

2. **Database Security**
   - Parameterized queries (SQLAlchemy ORM)
   - No SQL injection possible
   - Passwords hashed (future)

3. **API Security**
   - CORS configured
   - Rate limiting (future)
   - API key authentication (future)

4. **Data Privacy**
   - User data encrypted at rest (future)
   - HTTPS for all communications
   - GDPR compliant

## Scalability

### Horizontal Scaling
- Multiple Gunicorn workers
- Load balancer (Nginx/AWS ALB)
- Database replica for reads

### Vertical Scaling
- Increase server resources
- Upgrade database tier
- More Redis memory

### Caching Strategy
- Redis for session data
- Cache policies for 1 hour
- Cache API responses

### Database Optimization
- Indexing on frequently queried columns
- Query optimization
- Regular VACUUM & ANALYZE

## Performance Considerations

### Response Time Targets
- Chat response: < 2 seconds
- Lead creation: < 1 second
- WhatsApp send: < 3 seconds

### Optimization Techniques
- Lazy loading of policies
- Async WhatsApp sending (future)
- Database query caching
- Frontend code minification

## Monitoring & Observability

### Metrics to Track
- Response times
- Error rates
- Database queries
- Active users
- WhatsApp delivery rates

### Logging Strategy
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized log aggregation (future)

### Alerting
- High error rates
- Database connection failures
- WhatsApp API failures
- System resource limits

## Future Enhancements

1. **Machine Learning**
   - Better intent recognition
   - Personalized recommendations
   - Sentiment analysis

2. **Mobile App**
   - Native iOS/Android apps
   - Offline capabilities
   - Push notifications

3. **Advanced Features**
   - Video consultations
   - Document upload & analysis
   - Multi-language support

4. **Integration**
   - CRM system integration
   - Payment gateway
   - Logistics partner APIs

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Backend | Python, Flask, SQLAlchemy |
| Database | PostgreSQL, SQLite |
| Cache | Redis |
| AI/ML | OpenAI, Google AI |
| Messaging | Twilio (WhatsApp) |
| Deployment | Docker, Docker Compose |
| Server | Gunicorn, Nginx |
| Infrastructure | AWS EC2, RDS, S3 |

---

## Code Quality Standards

- **Python Style**: PEP 8
- **Code Coverage**: Minimum 80%
- **Testing**: Unit + Integration tests
- **Documentation**: Docstrings + README
- **Git Workflow**: Feature branches + PR review

