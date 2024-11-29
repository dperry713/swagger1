from flask import request
from flask_restx import Namespace, Resource, fields, abort
from ..models.models import db, Machine, Factory

machine_ns = Namespace('machines', description='Machine operations')

machine_model = machine_ns.model('Machine', {
    'id': fields.Integer(readonly=True, description='Machine unique identifier'),
    'name': fields.String(required=True, description='Machine name'),
    'type': fields.String(required=True, description='Machine type'),
    'factory_id': fields.Integer(required=True, description='Factory ID')
})

machine_input_model = machine_ns.model('MachineInput', {
    'name': fields.String(required=True, description='Machine name'),
    'type': fields.String(required=True, description='Machine type'),
    'factory_id': fields.Integer(required=True, description='Factory ID')
})

@machine_ns.route('/')
class MachineList(Resource):
    @machine_ns.doc('list_machines', 
                    responses={
                        200: 'Successful retrieval of machines',
                        500: 'Internal server error'
                    })
    @machine_ns.marshal_list_with(machine_model)
    def get(self):
        """List all machines"""
        try:
            machines = Machine.query.all()
            return [m.to_dict() for m in machines]
        except Exception as e:
            abort(500, f'Error retrieving machines: {str(e)}')

    @machine_ns.doc('create_machine', 
                    responses={
                        201: 'Machine created successfully',
                        400: 'Invalid input',
                        404: 'Factory not found',
                        500: 'Internal server error'
                    })
    @machine_ns.expect(machine_input_model)
    @machine_ns.marshal_with(machine_model, code=201)
    def post(self):
        """Create a new machine"""
        try:
            data = request.json
            if not data or 'name' not in data or 'type' not in data or 'factory_id' not in data:
                abort(400, 'Missing required fields')

            # Validate factory exists
            factory = Factory.query.get(data['factory_id'])
            if not factory:
                abort(404, f"Factory with ID {data['factory_id']} not found")

            new_machine = Machine(
                name=data['name'], 
                type=data['type'], 
                factory_id=data['factory_id']
            )
            db.session.add(new_machine)
            db.session.commit()
            return new_machine.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error creating machine: {str(e)}')

@machine_ns.route('/<int:machine_id>')
class MachineResource(Resource):
    @machine_ns.doc('get_machine', 
                    responses={
                        200: 'Successful retrieval of machine',
                        404: 'Machine not found',
                        500: 'Internal server error'
                    })
    @machine_ns.marshal_with(machine_model)
    def get(self, machine_id):
        """Retrieve a specific machine by ID"""
        try:
            machine = Machine.query.get_or_404(machine_id)
            return machine.to_dict()
        except Exception as e:
            abort(500, f'Error retrieving machine: {str(e)}')

    @machine_ns.doc('update_machine', 
                    responses={
                        200: 'Machine updated successfully',
                        400: 'Invalid input',
                        404: 'Machine not found',
                        500: 'Internal server error'
                    })
    @machine_ns.expect(machine_input_model)
    @machine_ns.marshal_with(machine_model)
    def put(self, machine_id):
        """Update an existing machine"""
        try:
            data = request.json
            if not data or all(key not in data for key in ['name', 'type', 'factory_id']):
                abort(400, 'No update fields provided')

            machine = Machine.query.get_or_404(machine_id)
            
            # Validate factory if provided
            if 'factory_id' in data:
                factory = Factory.query.get(data['factory_id'])
                if not factory:
                    abort(404, f"Factory with ID {data['factory_id']} not found")
                machine.factory_id = data['factory_id']

            # Update other fields if provided
            machine.name = data.get('name', machine.name)
            machine.type = data.get('type', machine.type)
            
            db.session.commit()
            return machine.to_dict()
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error updating machine: {str(e)}')

    @machine_ns.doc('delete_machine', 
                    responses={
                        204: 'Machine deleted successfully',
                        404: 'Machine not found',
                        500: 'Internal server error'
                    })
    def delete(self, machine_id):
        """Delete a machine"""
        try:
            machine = Machine.query.get_or_404(machine_id)
            db.session.delete(machine)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error deleting machine: {str(e)}')
