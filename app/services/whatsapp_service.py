import os
from dotenv import load_dotenv
from twilio.rest import Client
from app import db
from app.models import Lead

# Ensure .env is loaded
load_dotenv()

class WhatsAppService:
    """Handle WhatsApp integration via Twilio"""
    
    def __init__(self):
        # Force reload from environment
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', '').strip()
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', '').strip()
        self.whatsapp_from = os.getenv('TWILIO_WHATSAPP_NUMBER', '').strip()
        
        # Initialize Twilio client if credentials provided
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
    
    def send_message(self, to_number, message):
        """
        Send WhatsApp message via Twilio
        
        Args:
            to_number: Phone number in format +1234567890 or 91xxxxxxxxxx
            message: Message text to send
        
        Returns:
            dict with success status and message ID
        """
        try:
            # Ensure phone number has country code
            if not to_number.startswith('+'):
                if not to_number.startswith('91'):
                    to_number = '+91' + to_number
                else:
                    to_number = '+' + to_number
            
            if self.client:
                # Send via Twilio
                msg = self.client.messages.create(
                    from_=self.whatsapp_from,
                    body=message,
                    to=f'whatsapp:{to_number}'
                )
                return {
                    'success': True,
                    'message_id': msg.sid,
                    'status': 'sent'
                }
            else:
                # Demo mode - just log
                print(f"[DEMO] WhatsApp to {to_number}: {message}")
                return {
                    'success': True,
                    'message_id': 'demo_' + str(int(__import__('time').time())),
                    'status': 'demo'
                }
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return {
                'success': False,
                'error': str(e),
                'status': 'failed'
            }
    
    def send_to_lead(self, lead_id, message):
        """
        Send WhatsApp message to a lead
        
        Args:
            lead_id: Lead ID from database
            message: Message to send
        
        Returns:
            dict with success status
        """
        try:
            lead = Lead.query.get(lead_id)
            if not lead:
                return {'success': False, 'error': 'Lead not found'}
            
            if not lead.phone:
                return {'success': False, 'error': 'No phone number for lead'}
            
            result = self.send_message(lead.phone, message)
            
            if result['success']:
                lead.whatsapp_sent = True
                lead.whatsapp_message_id = result['message_id']
                db.session.commit()
            
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_admin_notification(self, subject, message, admin_phone):
        """
        Send notification to admin about new lead
        
        Args:
            subject: Subject of notification
            message: Message body
            admin_phone: Admin phone number
        
        Returns:
            dict with success status
        """
        full_message = f"🔔 {subject}\n\n{message}"
        return self.send_message(admin_phone, full_message)
    
    def handle_incoming_message(self, from_number, message_body):
        """
        Handle incoming WhatsApp messages (webhook handler)
        
        Args:
            from_number: Sender's phone number
            message_body: Message content
        
        Returns:
            dict with response message
        """
        # This would connect to your message processing logic
        # For now, return acknowledgment
        return {
            'status': 'received',
            'from': from_number,
            'message': message_body,
            'response': 'Thanks for your message. Our team will respond shortly.'
        }
