from flask import Flask
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    # Register routes
    from app.routes import user_blueprint
    app.register_blueprint(user_blueprint)

    return app
