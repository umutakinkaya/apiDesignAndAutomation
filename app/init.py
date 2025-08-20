from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('apiConfig.Config')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.sitesApi import sites_bp
    from app.routes.buildingsApi import buildings_bp
    from app.routes.levelsApi import levels_bp
    
    app.register_blueprint(sites_bp, url_prefix='/v1')
    app.register_blueprint(buildings_bp, url_prefix='/v1')
    app.register_blueprint(levels_bp, url_prefix='/v1')
    

    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    # Application context içinde database tablolarını oluştur
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables initialized")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    return app