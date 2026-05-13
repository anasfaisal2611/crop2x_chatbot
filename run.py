import os
import shutil
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
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
    if 'text/html' in request.headers.get('Accept', ''):
        try:
            return render_template('chatbot.html')
        except:
            pass
    return {'status': 'Crop2X API is running'}

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

@app.route('/api/chatbot/admin/upload-policy', methods=['POST'])
def upload_policy():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    shutil.copy2(file_path, os.path.join(upload_dir, 'current_policy.pdf'))

    try:
        scanner = PDFPolicyScanner(file_path)
        scanner.extract_policies()
        text = scanner.policies.get('content', '') or ''
        preview = (text.strip()[:400] + '…') if len(text.strip()) > 400 else text.strip()
        return jsonify({
            'success': True,
            'message': f'File "{filename}" was saved and set as the active knowledge document for the chatbot.',
            'extraction': {
                'pages': scanner.page_count,
                'characters': scanner.extracted_char_count,
                'has_readable_text': scanner.extracted_char_count > 0,
                'preview': preview or None,
            },
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'service': 'crop2x-backend'}, 200

if __name__ == '__main__':
    app.run(debug=True)