import pytest
from app import create_app, db
from app.models import Lead

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

def test_whatsapp_send(client):
    """Test sending WhatsApp message"""
    response = client.post('/api/whatsapp/send', json={
        'phone': '+919876543210',
        'message': 'Test message'
    })
    
    # Should return success even in test mode
    assert response.status_code == 200
    data = response.get_json()
    # Either success or demo mode
    assert 'success' in data

def test_whatsapp_send_to_lead(client):
    """Test sending WhatsApp to a lead"""
    # First create a lead
    lead_response = client.post('/api/leads/create', json={
        'name': 'Test Farmer',
        'email': 'test@example.com',
        'phone': '+919876543210',
        'location': 'Test Location',
        'lead_type': 'demo_request',
        'send_whatsapp': False
    })
    
    lead_id = lead_response.get_json()['lead_id']
    
    # Send WhatsApp to lead
    response = client.post(f'/api/whatsapp/send-to-lead/{lead_id}', json={
        'message': 'Hello from Crop2X!'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True

def test_whatsapp_webhook(client):
    """Test WhatsApp webhook"""
    response = client.post('/api/whatsapp/webhook', data={
        'From': 'whatsapp:+919876543210',
        'Body': 'Test incoming message'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
