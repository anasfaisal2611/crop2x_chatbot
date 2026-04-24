from flask import Blueprint, request, jsonify
from app import db
from app.models import User, ChatLog
from app.services.whatsapp_service import WhatsAppService

whatsapp_bp = Blueprint('whatsapp', __name__)
whatsapp_service = WhatsAppService()

@whatsapp_bp.route('/send', methods=['POST'])
def send_whatsapp():
    """Send WhatsApp message"""
    try:
        data = request.json
        phone = data.get('phone')
        message = data.get('message')
        lead_id = data.get('lead_id')
        
        if not phone or not message:
            return jsonify({
                'success': False,
                'error': 'Missing phone or message'
            }), 400
        
        result = whatsapp_service.send_message(phone, message)
        
        return jsonify({
            'success': result['success'],
            'message_id': result.get('message_id'),
            'status': result.get('status'),
            'error': result.get('error')
        }), 200 if result['success'] else 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whatsapp_bp.route('/send-to-lead/<int:lead_id>', methods=['POST'])
def send_to_lead(lead_id):
    """Send WhatsApp message to a specific lead"""
    try:
        data = request.json
        message = data.get('message')
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Missing message'
            }), 400
        
        result = whatsapp_service.send_to_lead(lead_id, message)
        
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whatsapp_bp.route('/webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    """Webhook for receiving WhatsApp messages from Twilio"""
    try:
        if request.method == 'GET':
            # Verification challenge
            return request.args.get('hub.challenge', ''), 200
        
        # Process incoming message
        data = request.form if request.form else request.json
        from_number = data.get('From', '').replace('whatsapp:', '')
        message_body = data.get('Body', '')
        
        # Handle the incoming message
        result = whatsapp_service.handle_incoming_message(from_number, message_body)
        
        # You can add message processing logic here
        # For now, we're just acknowledging receipt
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

@whatsapp_bp.route('/status/<message_id>', methods=['GET'])
def get_message_status(message_id):
    """Get status of sent WhatsApp message"""
    try:
        # This would integrate with Twilio's status tracking
        # For now, return a placeholder
        return jsonify({
            'success': True,
            'message_id': message_id,
            'status': 'delivered',  # Can be: queued, sent, delivered, failed
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whatsapp_bp.route('/send-bulk', methods=['POST'])
def send_bulk_messages():
    """Send bulk WhatsApp messages to multiple leads"""
    try:
        data = request.json
        recipients = data.get('recipients', [])  # List of {phone, message}
        
        if not recipients:
            return jsonify({
                'success': False,
                'error': 'No recipients provided'
            }), 400
        
        results = []
        for recipient in recipients:
            result = whatsapp_service.send_message(
                recipient.get('phone'),
                recipient.get('message')
            )
            results.append({
                'phone': recipient.get('phone'),
                'success': result['success'],
                'message_id': result.get('message_id')
            })
        
        success_count = sum(1 for r in results if r['success'])
        
        return jsonify({
            'success': True,
            'total': len(results),
            'successful': success_count,
            'results': results
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
