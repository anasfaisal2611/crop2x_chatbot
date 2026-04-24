from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import User, ChatLog
from app.services.ai_response_engine import AIResponseEngine
from app.services.whatsapp_service import WhatsAppService

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize services
ai_engine = AIResponseEngine()
whatsapp_service = WhatsAppService()

@chatbot_bp.route('/init', methods=['POST'])
def init_chat():
    """Initialize chatbot session"""
    try:
        data = request.json
        user_type = data.get('user_type', 'general')
        device_id = data.get('device_id')
        phone = data.get('phone')
        email = data.get('email')
        
        # Find or create user
        user = None
        if device_id:
            user = User.query.filter_by(device_id=device_id).first()
        elif phone:
            user = User.query.filter_by(phone_number=phone).first()
        elif email:
            user = User.query.filter_by(email=email).first()
        
        if not user:
            user = User(
                user_type=user_type,
                device_id=device_id,
                phone_number=phone,
                email=email
            )
            db.session.add(user)
            db.session.commit()
        else:
            user.user_type = user_type
            db.session.commit()
        
        return jsonify({
            'success': True,
            'user_id': user.id,
            'user_type': user.user_type,
            'message': 'Chat initialized successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/message', methods=['POST'])
def send_message():
    """Process user message and generate response"""
    try:
        data = request.json
        user_id = data.get('user_id')
        user_message = data.get('message', '').strip()
        
        if not user_id or not user_message:
            return jsonify({
                'success': False,
                'error': 'Missing user_id or message'
            }), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Generate AI response
        response_data = ai_engine.generate_response(
            user_query=user_message,
            user_type=user.user_type,
            context={'location': user.location}
        )
        
        # Store chat log
        chat_log = ChatLog(
            user_id=user_id,
            user_message=user_message,
            bot_response=response_data['message'],
            response_type=response_data.get('cta', 'text'),
            policies_used=response_data.get('policies_referenced', [])
        )
        db.session.add(chat_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'chat_id': chat_log.id,
            'response': response_data['message'],
            'next_action': response_data.get('next_action'),
            'cta': response_data.get('cta'),  # Call-to-action: 'whatsapp', 'lead_form', etc.
            'policies_referenced': response_data.get('policies_referenced', [])
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/history/<int:user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Get chat history for a user"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        chats = ChatLog.query.filter_by(user_id=user_id)\
            .order_by(ChatLog.created_at.desc())\
            .limit(limit)\
            .all()
        
        history = []
        for chat in reversed(chats):
            history.append({
                'id': chat.id,
                'user_message': chat.user_message,
                'bot_response': chat.bot_response,
                'timestamp': chat.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'count': len(history),
            'history': history
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/policies', methods=['GET'])
def get_policies():
    """Get available policies"""
    try:
        from app.services.pdf_policy_scanner import PDFPolicyScanner
        scanner = PDFPolicyScanner('')
        policies = scanner.get_cached_policies()
        
        if not policies:
            policies = scanner._get_dummy_policies()
        
        return jsonify({
            'success': True,
            'policies': policies
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
