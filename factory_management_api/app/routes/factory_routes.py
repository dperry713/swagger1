from flask import request
from flask_restx import Namespace, Resource, fields, abort
from ..models.models import db, Factory

factory_ns = Namespace('factories', description='Factory operations')

factory_model = factory_ns.model('Factory', {
    'id': fields.Integer(readonly=True, description='Factory unique identifier'),
    'name': fields.String(required=True, description='Factory name'),
    'location': fields.String(required=True, description='Factory location')
})

factory_input_model = factory_ns.model('FactoryInput', {
    'name': fields.String(required=True, description='Factory name'),
    'location': fields.String(required=True, description='Factory location')
})

@factory_ns.route('/')
class FactoryList(Resource):
    @factory_ns.doc('list_factories', 
                    responses={
                        200: 'Successful retrieval of factories',
                        500: 'Internal server error'
                    })
    @factory_ns.marshal_list_with(factory_model)
    def get(self):
        """List all factories"""
        try:
            factories = Factory.query.all()
            return [f.to_dict() for f in factories]
        except Exception as e:
            abort(500, f'Error retrieving factories: {str(e)}')

    @factory_ns.doc('create_factory', 
                    responses={
                        201: 'Factory created successfully',
                        400: 'Invalid input',
                        500: 'Internal server error'
                    })
    @factory_ns.expect(factory_input_model)
    @factory_ns.marshal_with(factory_model, code=201)
    def post(self):
        """Create a new factory"""
        try:
            data = request.json
            if not data or 'name' not in data or 'location' not in data:
                abort(400, 'Missing required fields')

            new_factory = Factory(name=data['name'], location=data['location'])
            db.session.add(new_factory)
            db.session.commit()
            return new_factory.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error creating factory: {str(e)}')

@factory_ns.route('/<int:factory_id>')
class FactoryResource(Resource):
    @factory_ns.doc('get_factory', 
                    responses={
                        200: 'Successful retrieval of factory',
                        404: 'Factory not found',
                        500: 'Internal server error'
                    })
    @factory_ns.marshal_with(factory_model)
    def get(self, factory_id):
        """Retrieve a specific factory by ID"""
        try:
            factory = Factory.query.get_or_404(factory_id)
            return factory.to_dict()
        except Exception as e:
            abort(500, f'Error retrieving factory: {str(e)}')

    @factory_ns.doc('update_factory', 
                    responses={
                        200: 'Factory updated successfully',
                        400: 'Invalid input',
                        404: 'Factory not found',
                        500: 'Internal server error'
                    })
    @factory_ns.expect(factory_input_model)
    @factory_ns.marshal_with(factory_model)
    def put(self, factory_id):
        """Update an existing factory"""
        try:
            data = request.json
            if not data or ('name' not in data and 'location' not in data):
                abort(400, 'Missing required fields')

            factory = Factory.query.get_or_404(factory_id)
            factory.name = data.get('name', factory.name)
            factory.location = data.get('location', factory.location)
            
            db.session.commit()
            return factory.to_dict()
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error updating factory: {str(e)}')

    @factory_ns.doc('delete_factory', 
                    responses={
                        204: 'Factory deleted successfully',
                        404: 'Factory not found',
                        500: 'Internal server error'
                    })
    def delete(self, factory_id):
        """Delete a factory"""
        try:
            factory = Factory.query.get_or_404(factory_id)
            db.session.delete(factory)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error deleting factory: {str(e)}')