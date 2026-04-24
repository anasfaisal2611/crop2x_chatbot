import os
from dotenv import load_dotenv

# Load environment variables FIRST - before anything else
load_dotenv()

from flask import render_template
from app import create_app, db
from app.services.pdf_policy_scanner import PDFPolicyScanner

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

@app.cli.command()
def init_db():
    """Initialize database"""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def seed_policies():
    """Seed policies from PDF"""
    pdf_path = os.getenv('POLICIES_PATH', 'policies/dummy_policies.pdf')
    scanner = PDFPolicyScanner(pdf_path)
    policies = scanner.extract_policies()
    print(f"Policies loaded: {list(policies.keys())}")

@app.route('/')
def index():
    """Serve chatbot page or API info based on request"""
    from flask import request
    if 'text/html' in request.headers.get('Accept', ''):
        try:
            return render_template('chatbot.html')
        except:
            pass
    
    return {
        'message': 'Crop2X Backend API',
        'version': '1.0.0',
        'endpoints': {
            'chatbot': '/api/chatbot',
            'whatsapp': '/api/whatsapp',
            'leads': '/api/leads'
        }
    }

@app.route('/chatbot')
def chatbot():
    """Serve chatbot HTML page"""
    return render_template('chatbot.html')

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'service': 'crop2x-backend'}, 200

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
