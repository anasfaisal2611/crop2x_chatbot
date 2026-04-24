from flask import Blueprint, request, jsonify
from app import db
from app.models import Lead, User
from app.services.ai_response_engine import AIResponseEngine
from app.services.whatsapp_service import WhatsAppService

leads_bp = Blueprint('leads', __name__)
ai_engine = AIResponseEngine()
whatsapp_service = WhatsAppService()

@leads_bp.route('/create', methods=['POST'])
def create_lead():
    """Create a new lead"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['name', 'email', 'location', 'lead_type']
        if not all(field in data for field in required):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required)}'
            }), 400
        
        user_id = data.get('user_id')
        
        # Create lead
        lead = Lead(
            user_id=user_id,
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            location=data['location'],
            farm_size=data.get('farm_size'),
            lead_type=data['lead_type'],
            message=data.get('message'),
            status='new'
        )
        
        db.session.add(lead)
        db.session.commit()
        
        # Generate WhatsApp message
        whatsapp_msg = ai_engine.generate_whatsapp_message({
            'name': data['name'],
            'lead_type': data['lead_type'],
            'location': data['location']
        })
        
        # Send WhatsApp if phone provided
        whatsapp_result = None
        if data.get('phone') and data.get('send_whatsapp', True):
            whatsapp_result = whatsapp_service.send_to_lead(lead.id, whatsapp_msg)
        
        return jsonify({
            'success': True,
            'lead_id': lead.id,
            'message': 'Lead created successfully',
            'whatsapp_sent': whatsapp_result and whatsapp_result.get('success', False)
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@leads_bp.route('/list', methods=['GET'])
def list_leads():
    """List all leads with filters"""
    try:
        status = request.args.get('status')
        lead_type = request.args.get('lead_type')
        limit = request.args.get('limit', 50, type=int)
        page = request.args.get('page', 1, type=int)
        
        query = Lead.query
        
        if status:
            query = query.filter_by(status=status)
        if lead_type:
            query = query.filter_by(lead_type=lead_type)
        
        total = query.count()
        leads = query.order_by(Lead.created_at.desc())\
            .limit(limit)\
            .offset((page - 1) * limit)\
            .all()
        
        leads_data = []
        for lead in leads:
            leads_data.append({
                'id': lead.id,
                'name': lead.name,
                'email': lead.email,
                'phone': lead.phone,
                'location': lead.location,
                'farm_size': lead.farm_size,
                'lead_type': lead.lead_type,
                'status': lead.status,
                'whatsapp_sent': lead.whatsapp_sent,
                'created_at': lead.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'total': total,
            'page': page,
            'limit': limit,
            'leads': leads_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@leads_bp.route('/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get specific lead details"""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
        
        return jsonify({
            'success': True,
            'lead': {
                'id': lead.id,
                'name': lead.name,
                'email': lead.email,
                'phone': lead.phone,
                'location': lead.location,
                'farm_size': lead.farm_size,
                'lead_type': lead.lead_type,
                'message': lead.message,
                'status': lead.status,
                'whatsapp_sent': lead.whatsapp_sent,
                'created_at': lead.created_at.isoformat(),
                'updated_at': lead.updated_at.isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@leads_bp.route('/<int:lead_id>/update-status', methods=['PUT'])
def update_lead_status(lead_id):
    """Update lead status"""
    try:
        data = request.json
        status = data.get('status')
        
        if not status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        lead = Lead.query.get(lead_id)
        if not lead:
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
        
        lead.status = status
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead_id': lead.id,
            'status': lead.status,
            'message': 'Lead status updated'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@leads_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get lead statistics"""
    try:
        from sqlalchemy import func
        
        total_leads = Lead.query.count()
        new_leads = Lead.query.filter_by(status='new').count()
        contacted = Lead.query.filter_by(status='contacted').count()
        converted = Lead.query.filter_by(status='converted').count()
        
        by_type = db.session.query(
            Lead.lead_type,
            func.count(Lead.id)
        ).group_by(Lead.lead_type).all()
        
        lead_types = {lt: count for lt, count in by_type}
        
        whatsapp_sent = Lead.query.filter_by(whatsapp_sent=True).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_leads': total_leads,
                'new': new_leads,
                'contacted': contacted,
                'converted': converted,
                'by_type': lead_types,
                'whatsapp_sent': whatsapp_sent
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
