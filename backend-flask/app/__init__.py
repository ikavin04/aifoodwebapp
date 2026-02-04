"""Flask application factory"""
from flask import Flask, jsonify
from app.config import config
from app.extensions import db, migrate, jwt, cors


def create_app(config_name='default'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    # Add request logging middleware
    @app.before_request
    def log_request_info():
        from flask import request
        import sys
        with open('f:/food app/aifoodwebapp/backend-flask/all_requests.log', 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"REQUEST: {request.method} {request.path}\n")
            f.write(f"Headers: {dict(request.headers)}\n")
            if request.get_json(silent=True):
                f.write(f"Body: {request.get_json()}\n")
            f.write(f"{'='*50}\n")
            f.flush()
    
    # JWT error handlers
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"INVALID TOKEN ERROR: {error}")
        return jsonify({'error': 'Invalid token', 'details': str(error)}), 401
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        print(f"UNAUTHORIZED ERROR: {error}")
        return jsonify({'error': 'Missing authorization header', 'details': str(error)}), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"EXPIRED TOKEN: header={jwt_header}, payload={jwt_payload}")
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        print(f"REVOKED TOKEN: header={jwt_header}, payload={jwt_payload}")
        return jsonify({'error': 'Token has been revoked'}), 401
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.restaurant import restaurant_bp
    from app.routes.cart import cart_bp
    from app.routes.order import order_bp
    from app.routes.ai_enhanced import ai_assistant_bp
    from app.routes.address import address_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(ai_assistant_bp)
    app.register_blueprint(address_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Food Ordering API',
            'version': '1.0.0',
            'status': 'running'
        }), 200
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    return app


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required or invalid credentials'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        import traceback
        import sys
        print(f"\n{'!'*50}", file=sys.stderr, flush=True)
        print(f"500 ERROR: {error}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        print(f"{'!'*50}\n", file=sys.stderr, flush=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(error),
            'details': traceback.format_exc()
        }), 500
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token Expired',
            'message': 'The access token has expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid Token',
            'message': 'The access token is invalid'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Missing Token',
            'message': 'Access token is missing'
        }), 401
