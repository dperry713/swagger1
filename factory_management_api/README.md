# Factory Management API

A RESTful API built with Flask and Swagger documentation for managing factory operations.

## Requirements

- Python 3.7+
- pip package manager

## Installation

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Features
RESTful API endpoints using Flask-RESTX
Interactive Swagger documentation
Database management with SQLAlchemy
Database migrations with Flask-Migrate
Environment variable configuration with python-dotenv
API Documentation
Once the server is running, access the Swagger documentation at: http://localhost:5000/api/docs

The API documentation is automatically generated using Flask-RESTX and provides:

Interactive endpoint testing
Request/Response models
Authentication requirements
Schema definitions
Environment Variables
Create a .env file in the root directory with:
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///factory.db
Running the Application
Start the development server:
flask run
Database Migrations
Initialize the database:
flask db init
Create a new migration:
flask db migrate -m "Initial migration"
Apply the migration:
flask db upgrade

This README provides a comprehensive guide for setting up and using the Factory Management API. The installed packages from requirements.txt enable:

- Flask-RESTX: Swagger documentation and API framework
- Flask-SQLAlchemy: Database ORM
- Flask-Migrate: Database migration management
- python-dotenv: Environment configuration

The Swagger UI will be automatically available at the /api/docs endpoint once the application is running.
