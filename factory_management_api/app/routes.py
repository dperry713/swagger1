from flask_restx import Resource, fields, Namespace
from .models.models import db, Customer, Employee, Product, Order, Production

def initialize_routes(api):
    # Namespaces
    customers_ns = api.namespace('customers', description='Customer operations')
    employees_ns = api.namespace('employees', description='Employee operations')
    products_ns = api.namespace('products', description='Product operations')
    orders_ns = api.namespace('orders', description='Order operations')
    production_ns = api.namespace('production', description='Production operations')

    # Customer Models
    customer_model = api.model('Customer', {
        'id': fields.Integer(readonly=True, description='The customer unique identifier'),
        'name': fields.String(required=True, description='Customer name'),
        'email': fields.String(required=True, description='Customer email'),
        'phone': fields.String(required=True, description='Customer phone number')
    })

    customer_input_model = api.model('CustomerInput', {
        'name': fields.String(required=True, description='Customer name'),
        'email': fields.String(required=True, description='Customer email'),
        'phone': fields.String(required=True, description='Customer phone number')
    })

    # Employees Routes (Example)
    @employees_ns.route('')
    class EmployeeList(Resource):
        @employees_ns.doc('list_employees')
        @employees_ns.marshal_list_with(customer_model)
        def get(self):
            """List all employees"""
            return [e.to_dict() for e in Employee.query.all()]

        @employees_ns.expect(customer_input_model)
        @employees_ns.marshal_with(customer_model, code=201)
        def post(self):
            """Create a new employee"""
            data = api.payload
            new_employee = Employee(name=data['name'], position=data['position'])
            db.session.add(new_employee)
            db.session.commit()
            return new_employee.to_dict(), 201

    # Similar routes for Customers, Products, Orders, and Production
    # Add them using similar methods
