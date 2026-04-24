from datetime import datetime
from app import db

class User(db.Model):
    """User model for chatbot interactions"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50), nullable=False)  # farmer, partner, enterprise
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    name = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    farm_size = db.Column(db.String(100), nullable=True)
    device_id = db.Column(db.String(200), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chat_logs = db.relationship('ChatLog', backref='user', lazy=True, cascade='all, delete-orphan')
    leads = db.relationship('Lead', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.id} - {self.user_type}>'

class ChatLog(db.Model):
    """Chat log model for storing conversation history"""
    __tablename__ = 'chat_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    response_type = db.Column(db.String(50), default='text')  # text, whatsapp_redirect, form
    policies_used = db.Column(db.JSON, nullable=True)  # Store which policies were referenced
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatLog {self.id} - User {self.user_id}>'

class Lead(db.Model):
    """Lead model for capturing demo requests and partnerships"""
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(200), nullable=False)
    farm_size = db.Column(db.String(100), nullable=True)
    lead_type = db.Column(db.String(50), nullable=False)  # demo_request, partnership, general_inquiry
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='new')  # new, contacted, converted, rejected
    whatsapp_sent = db.Column(db.Boolean, default=False)
    whatsapp_message_id = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lead {self.id} - {self.lead_type}>'

class PolicyCache(db.Model):
    """Cache for extracted policies from PDF"""
    __tablename__ = 'policy_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    policy_text = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.JSON, nullable=True)  # Store relevant keywords
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PolicyCache {self.id} - {self.category}>'
