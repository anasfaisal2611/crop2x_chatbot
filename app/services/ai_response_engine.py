import glob
import os
import re

from app.services.pdf_policy_scanner import PDFPolicyScanner


_SMALL_TALK = re.compile(
    r'''^\s*(
        hi|hello|hey|helo|hlw|hy|
        good\s*(morning|afternoon|evening|night)|
        salam|assalam|assalamu|assalamo|adaab|adab|namaste|namaskar|
        thanks|thank\s*you|thx|shukriya|shukria|meharbani|
        bye|goodbye|alvida|allah\s*hafiz|khuda\s*hafiz|
        ok|okay|theek|thik|tik|haan|han|ji|yes|no|nope|acha|accha|theek\s*hai
    )(\s|[,.!?]|$)''',
    re.IGNORECASE | re.VERBOSE,
)


def _is_small_talk(user_query: str) -> bool:
    q = (user_query or '').strip()
    if not q:
        return True
    if len(q) > 100:
        return False
    m = _SMALL_TALK.match(q)
    if m and m.end() == len(q):
        return True
    qlow = q.lower()
    if len(q) <= 50 and any(
        p in qlow for p in (
            'kaise ho', 'kaisy ho', 'kesay ho', 'kya hal', 'kya haal', 'ky haal',
            'kaisa hai', 'kaisi ho', 'sab theek', 'sab khairiyat',
        )
    ):
        return True
    return False


class AIResponseEngine:
    def __init__(self):
        self.scanner = PDFPolicyScanner('')

    @staticmethod
    def _active_policy_pdf():
        upload_dir = 'uploads'
        fixed = os.path.join(upload_dir, 'current_policy.pdf')
        if os.path.isfile(fixed):
            return fixed
        pdfs = glob.glob(os.path.join(upload_dir, '*.pdf'))
        if not pdfs:
            return None
        return max(pdfs, key=os.path.getctime)

    def _small_talk_response(self, user_type):
        lines = [
            'Hello! I am the Crop2X assistant.',
            'Great to hear from you — how can I help you today?',
            'You can ask about our services, or questions that relate to the document your administrator uploaded.',
        ]
        if not user_type or user_type == 'general':
            lines.append('For example: services, pricing, or how Crop2X can support you.')
        elif user_type == 'farmer':
            lines.append('I can help with crops, water savings, sensors, and pricing.')
        elif user_type == 'partner':
            lines.append('I can help with partnerships, commissions, and field data.')
        elif user_type == 'enterprise':
            lines.append('I can help with enterprise dashboards and integrations.')
        return {
            'response': '\n'.join(lines),
            'suggested_actions': ['1. Farmer', '2. Partner', '3. Enterprise'],
        }

    def generate_response(self, user_query, user_type='general', context=None):
        query = (user_query or '').strip()
        if _is_small_talk(query):
            return self._small_talk_response(user_type)

        pdf_path = self._active_policy_pdf()
        relevant_policies = {}

        if pdf_path:
            try:
                current_scanner = PDFPolicyScanner(pdf_path)
                relevant_policies = current_scanner.search_policies(query)
            except Exception as e:
                print(f"Scanning error: {e}")

        if relevant_policies.get('match'):
            pdf_text = str(relevant_policies['match'])
            if len(pdf_text) > 2800:
                pdf_text = pdf_text[:2800] + '\n\n...(message trimmed for length)...'
            return {
                'response': 'Here is the section from your knowledge document that best matches your question:\n\n' + pdf_text,
                'suggested_actions': ['Pricing Details', 'Contact Support', 'Main Menu'],
            }

        if relevant_policies.get('no_match'):
            return {
                'response': (
                    'I searched the uploaded document but could not find a clear answer for that question. '
                    'Try rephrasing with a few keywords from the topic, or ask your administrator to confirm the PDF contains readable text.\n\n'
                    'You can still use the suggested options below for general help.'
                ),
                'suggested_actions': ['Pricing Details', 'Contact Support', 'Main Menu'],
            }

        if pdf_path and not relevant_policies:
            try:
                scan = PDFPolicyScanner(pdf_path)
                data = scan.extract_policies()
                if not (data.get('content') or '').strip():
                    return {
                        'response': (
                            'A PDF is on file, but no text could be extracted — it may be a scanned image. '
                            'Please ask your administrator to upload a text-based PDF. Until then, I can still help with general topics below.'
                        ),
                        'suggested_actions': ['1. Farmer', '2. Partner', '3. Enterprise'],
                    }
            except Exception as e:
                print(f"PDF read error: {e}")

        if not user_type or user_type == 'general':
            return self._handle_general_query(query)

        responses = {
            'farmer': self._handle_farmer_query(query),
            'partner': self._handle_partner_query(query),
            'enterprise': self._handle_enterprise_query(query),
        }

        return responses.get(user_type, self._handle_general_query(query))

    def _handle_general_query(self, query):
        return {
            'response': (
                'Welcome to Crop2X. How can I help? '
                'You can ask about our services and pricing, or questions that relate to the policy document your team uploaded.'
            ),
            'suggested_actions': ['1. Farmer', '2. Partner', '3. Enterprise'],
        }

    def _handle_farmer_query(self, query):
        return {
            'response': (
                'I can help with crops, irrigation, and water savings. '
                'Ask about pricing or sensors anytime. For document-based answers, include words that appear in your uploaded PDF.'
            ),
            'suggested_actions': ['Water Management', 'Soil Health', 'Pricing'],
        }

    def _handle_partner_query(self, query):
        return {
            'response': (
                'Welcome to the partner area. Ask about commissions, leads, or field data. '
                'For answers from your uploaded PDF, include relevant keywords from the document.'
            ),
            'suggested_actions': ['Commission Structure', 'Lead Submission'],
        }

    def _handle_enterprise_query(self, query):
        return {
            'response': (
                'We offer custom dashboards and API integrations for enterprise customers. '
                'If your PDF uses specific technical terms, include them in your question for a better match.'
            ),
            'suggested_actions': ['Custom Dashboard', 'API Docs'],
        }

    def generate_whatsapp_message(self, lead_data):
        name = lead_data.get('name', 'Farmer')
        lead_type = lead_data.get('lead_type', 'inquiry')

        if lead_type == 'demo_request':
            message = f"Hello {name}! 👋 Thank you for requesting a demo of Crop2X!"
        elif lead_type == 'partnership':
            message = f"Hello {name}! 🤝 Thank you for your interest in partnering!"
        else:
            message = f"Hello {name}! 👋 Thank you for reaching out to Crop2X!"

        return message


ai_response_engine = AIResponseEngine()
