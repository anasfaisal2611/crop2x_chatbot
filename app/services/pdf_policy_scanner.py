import os
import re

import PyPDF2

from app import db
from app.models import PolicyCache


_STOPWORDS = frozenset({
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out',
    'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way',
    'who', 'did', 'she', 'use', 'many', 'then', 'them', 'will', 'what', 'with', 'have', 'this', 'that',
    'from', 'they', 'been', 'into', 'than', 'when', 'come', 'such', 'also', 'only', 'your', 'some',
    'time', 'very', 'about', 'after', 'tell', 'give', 'need', 'want', 'know', 'like', 'just', 'more',
    'kya', 'hai', 'hain', 'ka', 'ke', 'ki', 'ko', 'se', 'mein', 'par', 'bhi', 'agar', 'nahi', 'kahan',
    'kyun', 'kaise', 'kis', 'kisi', 'yeh', 'woh', 'hum', 'aap', 'mujhe', 'batao', 'bata', 'please',
})


class PDFPolicyScanner:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.policies = {}
        self.page_count = 0
        self.extracted_char_count = 0

    def extract_policies(self):
        """PDF se text nikaal kar save karna"""
        self.page_count = 0
        self.extracted_char_count = 0
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            print(f"DEBUG: File not found at {self.pdf_path}")
            return {}

        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                self.page_count = len(reader.pages)
                text = ""
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\n"

                self.extracted_char_count = len(text.strip())
                if text.strip():
                    self.policies = {"content": text}
                    print("--- PDF Data Loaded Successfully! ---")
                else:
                    print("--- Warning: PDF is empty or unreadable ---")
                return self.policies
        except Exception as e:
            print(f"DEBUG: PDF extraction error: {e}")
            return {}

    def _parse_policies(self, text):
        """Parse extracted text into categories"""
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
        """Cache policies in database - Clean state strategy"""
        from app import db
        from app.models import PolicyCache

        try:
            PolicyCache.query.delete()

            for category, policy_text in self.policies.items():
                cache = PolicyCache(category=category, policy_text=policy_text)
                db.session.add(cache)

            db.session.commit()
            print("Policies successfully updated in DB.")

        except Exception as e:
            db.session.rollback()
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

    @staticmethod
    def _query_keywords(query: str):
        """Meaningful tokens for matching (not full substring of question)."""
        words = re.findall(r'[a-z0-9]{2,}', (query or '').lower())
        return [w for w in words if w not in _STOPWORDS]

    def _chunk_text(self, content: str):
        """Split PDF text into searchable chunks."""
        normalized = re.sub(r'\r\n?', '\n', content)
        parts = [p.strip() for p in re.split(r'\n{2,}', normalized) if len(p.strip()) > 30]
        if len(parts) >= 2:
            return parts
        lines = [ln.strip() for ln in normalized.split('\n') if ln.strip()]
        chunks = []
        buf = []
        length = 0
        for ln in lines:
            buf.append(ln)
            length += len(ln) + 1
            if length >= 400:
                chunks.append('\n'.join(buf))
                buf = []
                length = 0
        if buf:
            chunks.append('\n'.join(buf))
        if not chunks and normalized.strip():
            return [normalized.strip()]
        return chunks

    def search_policies(self, query):
        """User ke sawal se related PDF hissa dhoondna (keyword / overlap)."""
        if not self.policies:
            self.extract_policies()

        content = self.policies.get('content', '')
        if not content.strip():
            return {}

        query_l = (query or '').lower().strip()
        hay = content.lower()

        if query_l and query_l in hay:
            idx = hay.find(query_l)
            start = max(0, idx - 120)
            end = min(len(content), idx + len(query_l) + 900)
            return {'match': content[start:end].strip()}

        keywords = self._query_keywords(query)
        if not keywords:
            return {}

        chunks = self._chunk_text(content)
        best_chunk = None
        best_score = 0

        for chunk in chunks:
            cl = chunk.lower()
            score = 0
            for kw in keywords:
                if kw in cl:
                    score += 1 + min(2, cl.count(kw) // 3)
            if score > best_score:
                best_score = score
                best_chunk = chunk

        min_score = 1 if len(keywords) <= 2 else 2
        if best_chunk is not None and best_score >= min_score:
            excerpt = best_chunk.strip()
            if len(excerpt) > 2000:
                excerpt = excerpt[:2000] + '\n\n...(remaining text omitted)...'
            return {'match': excerpt}

        return {'no_match': True}

    @staticmethod
    def get_cached_policies():
        """Get policies from cache"""
        policies = {}
        cached = PolicyCache.query.all()
        for cache in cached:
            policies[cache.category] = cache.policy_text
        return policies
