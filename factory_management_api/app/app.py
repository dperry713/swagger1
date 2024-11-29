from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure API
    api = Api(app, 
        title='Factory Management API',
        version='1.0',
        description='A comprehensive Factory Management System API',
        doc='/'
    )

    # Import and register namespaces
    from .routes.factory_routes import factory_ns
    from .routes.machine_routes import machine_ns
    from .routes.worker_routes import worker_ns

    api.add_namespace(factory_ns, path='/factories')
    api.add_namespace(machine_ns, path='/machines')
    api.add_namespace(worker_ns, path='/workers')

    return app