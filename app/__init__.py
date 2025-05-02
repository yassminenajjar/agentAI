from flask import Flask
from Config import config  # Import from root level
from app.models.database import db_instance

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    db_instance.init_app(app)
    
    with app.app_context():
        from app.route.routes import query_blueprint
        app.register_blueprint(query_blueprint, url_prefix='/api')
    
    return app