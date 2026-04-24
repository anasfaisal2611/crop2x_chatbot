import PyPDF2
import os
from datetime import datetime
from app import db
from app.models import PolicyCache

class PDFPolicyScanner:
    """Scans and extracts policies from PDF files"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.policies = {}
    
    def extract_policies(self):
        """Extract all text from PDF"""
        try:
            if not os.path.exists(self.pdf_path):
                return self._get_dummy_policies()
            
            text = ""
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            self._parse_policies(text)
            self._cache_policies()
            return self.policies
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return self._get_dummy_policies()
    
    def _parse_policies(self, text):
        """Parse extracted text into categories"""
        # Split by common section headers
        sections = {
            'water_conservation': self._extract_section(text, ['water', 'irrigation', 'conservation']),
            'crop_support': self._extract_section(text, ['crops', 'supported', 'varieties']),
            'partnership': self._extract_section(text, ['partner', 'partnership', 'collaboration']),
            'sustainability': self._extract_section(text, ['sustainable', 'environment', 'eco']),
            'pricing': self._extract_section(text, ['price', 'cost', 'pricing', 'subscription']),
        }
        
        self.policies = {k: v for k, v in sections.items() if v}
    
    def _extract_section(self, text, keywords):
        """Extract section based on keywords"""
        lines = text.split('\n')
        section_text = ""
        capture = False
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                capture = True
            elif capture and any(keyword in line_lower for keyword in ['section', 'policy', '##', '---']):
                break
            
            if capture:
                section_text += line + "\n"
        
        return section_text.strip()[:500] if section_text else None
    
    def _cache_policies(self):
        """Cache policies in database"""
        try:
            for category, policy_text in self.policies.items():
                existing = PolicyCache.query.filter_by(category=category).first()
                if existing:
                    existing.policy_text = policy_text
                    existing.last_updated = datetime.utcnow()
                else:
                    cache = PolicyCache(category=category, policy_text=policy_text)
                    db.session.add(cache)
            db.session.commit()
        except Exception as e:
            print(f"Error caching policies: {e}")
    
    def _get_dummy_policies(self):
        """Return dummy policies for testing"""
        return {
            'water_conservation': '''
            Crop2X Water Conservation Policy:
            - We help farmers reduce water usage by 40-60% using AI-powered irrigation optimization
            - Drip irrigation systems are supported for all major crops
            - Smart sensors provide real-time soil moisture data
            - Our platform integrates with existing irrigation infrastructure
            ''',
            'crop_support': '''
            Supported Crops:
            - Wheat: High yield variety optimization
            - Rice: Water-efficient farming techniques
            - Cotton: Pest management and yield prediction
            - Sugarcane: Growth monitoring and harvesting optimization
            - Vegetables: Seasonal crop planning and management
            - Pulses: Sustainability and nutrition-focused farming
            ''',
            'partnership': '''
            Partnership Program:
            - Join Crop2X to expand your agricultural services
            - Revenue sharing model: 20-30% commission
            - Dedicated partner support team
            - White-label solutions available
            - Training and certification provided
            - Minimum commitment: 100 farmers per month
            ''',
            'sustainability': '''
            Sustainability Initiatives:
            - Carbon footprint reduction through efficient farming
            - Eco-friendly pest management solutions
            - Soil health monitoring and improvement
            - Water conservation leading to 50% usage reduction
            - Biodiversity support through crop rotation planning
            ''',
            'pricing': '''
            Pricing Models:
            - Free tier: Basic chatbot and limited features
            - Farmer Plan: Rs. 500/month - Full AI features, water optimization
            - Enterprise Plan: Custom pricing - Full customization, API access
            - Partnership Plan: Commission-based model with revenue sharing
            '''
        }
    
    def search_policies(self, query):
        """Search policies for relevant information"""
        results = {}
        query_lower = query.lower()
        
        for category, policy_text in self.policies.items():
            if query_lower in policy_text.lower():
                results[category] = policy_text
        
        return results if results else self.policies
    
    @staticmethod
    def get_cached_policies():
        """Get policies from cache"""
        policies = {}
        cached = PolicyCache.query.all()
        for cache in cached:
            policies[cache.category] = cache.policy_text
        return policies
