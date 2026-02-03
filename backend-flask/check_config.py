from app import create_app

app = create_app()

with app.app_context():
    print("=== JWT Configuration ===")
    print(f"JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')}")
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
    print(f"JWT_TOKEN_LOCATION: {app.config.get('JWT_TOKEN_LOCATION')}")
    print(f"JWT_HEADER_NAME: {app.config.get('JWT_HEADER_NAME')}")
    print(f"JWT_HEADER_TYPE: {app.config.get('JWT_HEADER_TYPE')}")
    print(f"JWT_COOKIE_CSRF_PROTECT: {app.config.get('JWT_COOKIE_CSRF_PROTECT')}")
