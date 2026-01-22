"""
Flask Application - AI Food Ordering System
"""

from flask import Flask
from ai_assistant import ai_assistant_bp


def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    app.register_blueprint(ai_assistant_bp)
    
    @app.route('/')
    def home():
        return {
            'message': 'AI Food Ordering System API',
            'version': '1.0',
            'endpoints': {
                'ai_assistant': '/ai/order-assistant',
                'payment_query': '/ai/payment-query'
            }
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    @app.route('/favicon.ico')
    def favicon():
        """Return empty response to prevent 404 errors"""
        return '', 204
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("Starting Flask server...")
    print("AI Assistant endpoint: http://localhost:5000/ai/order-assistant")
    app.run(debug=True, host='0.0.0.0', port=5000)
