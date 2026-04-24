import re

class Validators:
    """Validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        # Remove common separators
        phone_clean = re.sub(r'[\s\-\+\(\)]', '', phone)
        # Check if it contains 10+ digits
        return re.search(r'\d{10,}', phone_clean) is not None
    
    @staticmethod
    def validate_user_type(user_type):
        """Validate user type"""
        valid_types = ['farmer', 'partner', 'enterprise', 'general']
        return user_type.lower() in valid_types
    
    @staticmethod
    def validate_lead_type(lead_type):
        """Validate lead type"""
        valid_types = ['demo_request', 'partnership', 'general_inquiry']
        return lead_type.lower() in valid_types
    
    @staticmethod
    def sanitize_input(text, max_length=1000):
        """Sanitize user input"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Limit length
        text = text[:max_length]
        # Remove excessive whitespace
        text = ' '.join(text.split())
        return text
