import os
from datetime import datetime
from app.services.pdf_policy_scanner import PDFPolicyScanner

class AIResponseEngine:
    """Generate AI responses based on policies and user context"""
    
    def __init__(self):
        self.pdf_path = os.getenv('POLICIES_PATH', 'policies/dummy_policies.pdf')
        self.scanner = PDFPolicyScanner(self.pdf_path)
        self.policies = self.scanner.extract_policies()
    
    def generate_response(self, user_query, user_type, context=None):
        """
        Generate response based on user query and policies
        
        Args:
            user_query: The user's question
            user_type: farmer, partner, or enterprise
            context: Additional context about the user
        
        Returns:
            dict with response and suggested actions
        """
        # Search relevant policies
        relevant_policies = self.scanner.search_policies(user_query)
        
        # Generate response based on query type
        query_lower = user_query.lower()
        
        if user_type == 'farmer':
            response = self._handle_farmer_query(query_lower, relevant_policies)
        elif user_type == 'partner':
            response = self._handle_partner_query(query_lower, relevant_policies)
        elif user_type == 'enterprise':
            response = self._handle_enterprise_query(query_lower, relevant_policies)
        else:
            response = self._handle_general_query(query_lower, relevant_policies)
        
        return response
    
    def _handle_farmer_query(self, query, policies):
        """Handle farmer-specific queries"""
        response = {
            'message': '',
            'next_action': '',
            'policies_referenced': list(policies.keys()),
            'cta': None
        }
        
        if any(word in query for word in ['water', 'irrigation', 'save']):
            response['message'] = f"""
            🌾 Water Conservation:
            
            {policies.get('water_conservation', 'Based on our policies, we help farmers reduce water usage significantly.')}
            
            Key Benefits:
            ✓ 40-60% water usage reduction
            ✓ Real-time soil moisture monitoring
            ✓ Smart irrigation scheduling
            ✓ Cost savings of Rs. 50,000+ per season
            
            Would you like to know more about how this works?
            """
            response['cta'] = 'whatsapp'
            response['next_action'] = 'Lead to WhatsApp for detailed demo'
        
        elif any(word in query for word in ['crops', 'support', 'varieties', 'what crops']):
            response['message'] = f"""
            🌱 Supported Crops:
            
            {policies.get('crop_support', 'We support various crops with optimization features.')}
            
            Each crop has:
            ✓ Yield prediction models
            ✓ Pest management guidance
            ✓ Optimal planting schedules
            ✓ Market price tracking
            
            Which crop are you interested in?
            """
            response['cta'] = 'lead_form'
            response['next_action'] = 'Collect farm details'
        
        elif any(word in query for word in ['price', 'cost', 'subscription', 'plan']):
            response['message'] = f"""
            💰 Pricing for Farmers:
            
            {policies.get('pricing', 'We offer flexible pricing options.')}
            
            Free Trial: 30 days - No credit card required
            Premium: Rs. 500/month - Full features
            
            Let's get you started!
            """
            response['cta'] = 'lead_form'
            response['next_action'] = 'Setup subscription'
        
        else:
            response['message'] = f"""
            🌾 Hello Farmer!
            
            I can help you with:
            ✓ Water conservation strategies
            ✓ Crop selection and management
            ✓ Yield optimization
            ✓ Pest and disease management
            
            You can also reach our team on WhatsApp for personalized support.
            
            What would you like to know about?
            """
            response['cta'] = 'whatsapp'
            response['next_action'] = 'Direct to WhatsApp for support'
        
        return response
    
    def _handle_partner_query(self, query, policies):
        """Handle partner-specific queries"""
        response = {
            'message': '',
            'next_action': '',
            'policies_referenced': list(policies.keys()),
            'cta': None
        }
        
        if any(word in query for word in ['partner', 'partnership', 'collaborate', 'join']):
            response['message'] = f"""
            🤝 Partnership Opportunities:
            
            {policies.get('partnership', 'Learn about our partnership program.')}
            
            Why Partner with Crop2X?
            ✓ 20-30% Commission on each farmer
            ✓ Dedicated support team
            ✓ Marketing support and materials
            ✓ White-label solutions available
            ✓ Monthly payouts
            
            Let's discuss your partnership goals!
            """
            response['cta'] = 'lead_form'
            response['next_action'] = 'Collect partnership details'
        
        elif any(word in query for word in ['revenue', 'earning', 'commission']):
            response['message'] = f"""
            💹 Revenue Model:
            
            {policies.get('partnership', 'Our revenue sharing works as follows.')}
            
            Earning Potential:
            - Commission: 20-30% per active farmer
            - Bonus: 5% extra for 50+ farmers
            - Recurring revenue model
            
            Example: With 100 farmers at Rs. 500/month
            Monthly revenue: Rs. 25,000 - 37,500
            
            Interested in the details?
            """
            response['cta'] = 'whatsapp'
            response['next_action'] = 'Connect to business team'
        
        else:
            response['message'] = f"""
            🤝 Welcome, Partner!
            
            I can provide information on:
            ✓ Partnership programs and benefits
            ✓ Revenue sharing models
            ✓ Integration and technical details
            ✓ Support and training
            
            For detailed discussions, let's connect you with our partnership team!
            """
            response['cta'] = 'whatsapp'
            response['next_action'] = 'Direct to WhatsApp'
        
        return response
    
    def _handle_enterprise_query(self, query, policies):
        """Handle enterprise-specific queries"""
        response = {
            'message': '',
            'next_action': '',
            'policies_referenced': list(policies.keys()),
            'cta': None
        }
        
        response['message'] = f"""
        🏢 Enterprise Solutions:
        
        We provide custom solutions including:
        ✓ White-label platform
        ✓ Custom API integration
        ✓ Dedicated support team
        ✓ Advanced analytics and reporting
        ✓ Multiple user management
        ✓ SLA guarantees
        
        Our enterprise team will work directly with you to customize a solution.
        """
        response['cta'] = 'lead_form'
        response['next_action'] = 'Collect enterprise requirements'
        
        return response
    
    def _handle_general_query(self, query, policies):
        """Handle general queries"""
        response = {
            'message': f"""
            👋 Welcome to Crop2X!
            
            Are you a:
            1️⃣ Farmer - Looking to optimize your crops?
            2️⃣ Partner - Interested in partnership?
            3️⃣ Enterprise - Need custom solutions?
            
            Or tell me your question and I'll help!
            
            {policies.get('sustainability', 'Our platform helps with sustainable farming.')}
            """,
            'next_action': 'Classify user type',
            'policies_referenced': list(policies.keys()),
            'cta': 'whatsapp'
        }
        
        return response
    
    def generate_whatsapp_message(self, lead_data):
        """Generate WhatsApp message for lead"""
        name = lead_data.get('name', 'Farmer')
        lead_type = lead_data.get('lead_type', 'inquiry')
        
        if lead_type == 'demo_request':
            message = f"""
Hello {name}! 👋

Thank you for requesting a demo of Crop2X!

We're excited to show you how to:
✓ Save 40-60% water
✓ Increase yields by 25-35%
✓ Reduce farming costs

Our specialist will connect with you shortly to schedule a personalized demo.

In the meantime, visit: https://crop2x.com/features

Questions? Reply to this message!

Crop2X Team 🌾
            """
        elif lead_type == 'partnership':
            message = f"""
Hello {name}! 🤝

Thank you for your interest in partnering with Crop2X!

Partnership benefits:
✓ 20-30% commission per farmer
✓ Dedicated support team
✓ Marketing materials provided
✓ Monthly payouts

Our partnership manager will contact you within 24 hours to discuss opportunities.

Learn more: https://crop2x.com/partners

Crop2X Team 🌾
            """
        else:
            message = f"""
Hello {name}! 👋

Thank you for reaching out to Crop2X!

We're here to help with:
✓ Agricultural consulting
✓ Crop optimization
✓ Technology solutions
✓ Partnership opportunities

Our team will get back to you within 2 hours.

Visit us: https://crop2x.com

Crop2X Team 🌾
            """
        
        return message.strip()
