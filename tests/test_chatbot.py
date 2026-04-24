import pytest
from app import create_app, db
from app.models import User, ChatLog

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

def test_chatbot_init(client):
    """Test chatbot initialization"""
    response = client.post('/api/chatbot/init', json={
        'user_type': 'farmer',
        'device_id': 'test_device_123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert data['user_id'] is not None

def test_send_message(client):
    """Test sending message to chatbot"""
    # First initialize
    init_response = client.post('/api/chatbot/init', json={
        'user_type': 'farmer'
    })
    user_id = init_response.get_json()['user_id']
    
    # Send message
    response = client.post('/api/chatbot/message', json={
        'user_id': user_id,
        'message': 'How can I save water?'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert data['response'] is not None

def test_create_lead(client):
    """Test creating a lead"""
    response = client.post('/api/leads/create', json={
        'name': 'Raj Farmer',
        'email': 'raj@example.com',
        'phone': '+919876543210',
        'location': 'Punjab',
        'lead_type': 'demo_request',
        'send_whatsapp': False
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] == True
    assert data['lead_id'] is not None

def test_get_policies(client):
    """Test getting policies"""
    response = client.get('/api/chatbot/policies')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'policies' in data
