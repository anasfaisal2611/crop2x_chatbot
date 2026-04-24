# API Specification Document

## Base URL
```
http://localhost:5000/api
```

---

## Chatbot API

### 1. Initialize Chat Session
**Endpoint:** `POST /chatbot/init`

**Request:**
```json
{
  "user_type": "farmer|partner|enterprise|general",
  "device_id": "device_123",
  "phone": "+919876543210",
  "email": "user@example.com"
}
```

**Response (Success):**
```json
{
  "success": true,
  "user_id": 1,
  "user_type": "farmer",
  "message": "Chat initialized successfully"
}
```

**Status Codes:** 
- 200: Success
- 400: Bad request
- 500: Server error

---

### 2. Send Message to Chatbot
**Endpoint:** `POST /chatbot/message`

**Request:**
```json
{
  "user_id": 1,
  "message": "How can I save water?"
}
```

**Response (Success):**
```json
{
  "success": true,
  "chat_id": 1,
  "response": "🌾 Water Conservation:\n\n...",
  "next_action": "Lead to WhatsApp for detailed demo",
  "cta": "whatsapp|lead_form|none",
  "policies_referenced": ["water_conservation", "pricing"]
}
```

**CTA Types:**
- `whatsapp`: Show WhatsApp connection option
- `lead_form`: Show lead form
- `none`: No call-to-action

---

### 3. Get Chat History
**Endpoint:** `GET /chatbot/history/{user_id}`

**Query Parameters:**
- `limit`: Number of messages (default: 50)

**Response:**
```json
{
  "success": true,
  "count": 5,
  "history": [
    {
      "id": 1,
      "user_message": "How can I save water?",
      "bot_response": "🌾 Water Conservation...",
      "timestamp": "2024-04-20T10:30:00"
    }
  ]
}
```

---

### 4. Get Available Policies
**Endpoint:** `GET /chatbot/policies`

**Response:**
```json
{
  "success": true,
  "policies": {
    "water_conservation": "Crop2X Water Conservation Policy...",
    "crop_support": "Supported Crops...",
    "partnership": "Partnership Program...",
    "pricing": "Pricing Models..."
  }
}
```

---

## Lead Management API

### 1. Create Lead
**Endpoint:** `POST /leads/create`

**Request:**
```json
{
  "user_id": 1,
  "name": "Raj Farmer",
  "email": "raj@example.com",
  "phone": "+919876543210",
  "location": "Punjab",
  "farm_size": "5 acres",
  "lead_type": "demo_request|partnership|general_inquiry",
  "message": "I want to join the demo",
  "send_whatsapp": true
}
```

**Required Fields:**
- name
- email
- location
- lead_type

**Response (Success):**
```json
{
  "success": true,
  "lead_id": 1,
  "message": "Lead created successfully",
  "whatsapp_sent": true
}
```

**Status Codes:**
- 201: Created
- 400: Bad request
- 500: Server error

---

### 2. List Leads
**Endpoint:** `GET /leads/list`

**Query Parameters:**
- `status`: new|contacted|converted|rejected (optional)
- `lead_type`: demo_request|partnership|general_inquiry (optional)
- `limit`: Items per page (default: 50)
- `page`: Page number (default: 1)

**Response:**
```json
{
  "success": true,
  "total": 100,
  "page": 1,
  "limit": 50,
  "leads": [
    {
      "id": 1,
      "name": "Raj Farmer",
      "email": "raj@example.com",
      "phone": "+919876543210",
      "location": "Punjab",
      "farm_size": "5 acres",
      "lead_type": "demo_request",
      "status": "new",
      "whatsapp_sent": true,
      "created_at": "2024-04-20T10:00:00"
    }
  ]
}
```

---

### 3. Get Lead Details
**Endpoint:** `GET /leads/{lead_id}`

**Response:**
```json
{
  "success": true,
  "lead": {
    "id": 1,
    "name": "Raj Farmer",
    "email": "raj@example.com",
    "phone": "+919876543210",
    "location": "Punjab",
    "farm_size": "5 acres",
    "lead_type": "demo_request",
    "message": "Demo request message",
    "status": "new",
    "whatsapp_sent": true,
    "created_at": "2024-04-20T10:00:00",
    "updated_at": "2024-04-20T10:00:00"
  }
}
```

---

### 4. Update Lead Status
**Endpoint:** `PUT /leads/{lead_id}/update-status`

**Request:**
```json
{
  "status": "contacted|converted|rejected"
}
```

**Response:**
```json
{
  "success": true,
  "lead_id": 1,
  "status": "contacted",
  "message": "Lead status updated"
}
```

---

### 5. Get Lead Statistics
**Endpoint:** `GET /leads/stats`

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_leads": 150,
    "new": 50,
    "contacted": 60,
    "converted": 30,
    "by_type": {
      "demo_request": 80,
      "partnership": 40,
      "general_inquiry": 30
    },
    "whatsapp_sent": 120
  }
}
```

---

## WhatsApp Integration API

### 1. Send WhatsApp Message
**Endpoint:** `POST /whatsapp/send`

**Request:**
```json
{
  "phone": "+919876543210",
  "message": "Hello from Crop2X!",
  "lead_id": 1
}
```

**Response (Success):**
```json
{
  "success": true,
  "message_id": "SM1234567890abcdef",
  "status": "sent|demo",
  "error": null
}
```

**Status Codes:**
- 200: Success
- 400: Bad request
- 500: Server error

---

### 2. Send Message to Lead
**Endpoint:** `POST /whatsapp/send-to-lead/{lead_id}`

**Request:**
```json
{
  "message": "Hello from Crop2X!"
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "SM1234567890abcdef",
  "status": "sent"
}
```

---

### 3. Send Bulk Messages
**Endpoint:** `POST /whatsapp/send-bulk`

**Request:**
```json
{
  "recipients": [
    {
      "phone": "+919876543210",
      "message": "Hello Farmer!"
    },
    {
      "phone": "+919876543211",
      "message": "Hello Partner!"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "total": 2,
  "successful": 2,
  "results": [
    {
      "phone": "+919876543210",
      "success": true,
      "message_id": "SM1234567890"
    },
    {
      "phone": "+919876543211",
      "success": true,
      "message_id": "SM0987654321"
    }
  ]
}
```

---

### 4. WhatsApp Webhook
**Endpoint:** `POST /whatsapp/webhook`

**Incoming Webhook Data (from Twilio):**
```
From: whatsapp:+919876543210
Body: User's incoming message text
```

**Response:**
```json
{
  "status": "received",
  "from": "+919876543210",
  "message": "User's message",
  "response": "Thanks for your message. Our team will respond shortly."
}
```

---

### 5. Get Message Status
**Endpoint:** `GET /whatsapp/status/{message_id}`

**Response:**
```json
{
  "success": true,
  "message_id": "SM1234567890",
  "status": "queued|sent|delivered|failed",
  "timestamp": "2024-04-20T10:30:00"
}
```

---

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Description of the error"
}
```

### Common Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 400 | Missing required fields | Check request body |
| 404 | Resource not found | Verify ID exists |
| 500 | Server error | Check server logs |
| 422 | Validation error | Check data format |

---

## Authentication (Future)

Currently, the API has no authentication. In production, implement:

```
Authorization: Bearer {token}
```

---

## Rate Limiting (Future)

Planned rate limits:
- 100 requests per minute (public)
- 1000 requests per minute (authenticated)

---

## Pagination

For list endpoints:

```
GET /leads/list?page=1&limit=50
```

**Response includes:**
- `total`: Total number of items
- `page`: Current page
- `limit`: Items per page
- `items`: Array of results

---

## Versioning

Current API Version: **v1**

Future: Support `/api/v2`, `/api/v3`, etc.

---

## CORS Configuration

- **Origin:** * (configurable in .env)
- **Methods:** GET, POST, PUT, DELETE
- **Headers:** Content-Type, Authorization

---

## Testing Endpoints

### Health Check
```bash
GET /health
```

### Root Endpoint
```bash
GET /
```

---

## Request/Response Formats

### Content-Type
- All requests and responses use `application/json`
- Ensure `Content-Type: application/json` header in POST/PUT requests

### Date Format
- ISO 8601: `2024-04-20T10:30:00`

### Phone Number Format
- With country code: `+919876543210`
- Accepted formats: `+91 98765 43210`, `919876543210`

---

## Documentation Version
- Version: 1.0
- Last Updated: April 2024
- Next Review: July 2024
