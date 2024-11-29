from flask import request
from flask_restx import Namespace, Resource, fields, abort
from ..models.models import db, Worker, Factory

worker_ns = Namespace('workers', description='Worker operations')

worker_model = worker_ns.model('Worker', {
    'id': fields.Integer(readonly=True, description='Worker unique identifier'),
    'name': fields.String(required=True, description='Worker name'),
    'role': fields.String(required=True, description='Worker role'),
    'factory_id': fields.Integer(required=True, description='Factory ID')
})

worker_input_model = worker_ns.model('WorkerInput', {
    'name': fields.String(required=True, description='Worker name'),
    'role': fields.String(required=True, description='Worker role'),
    'factory_id': fields.Integer(required=True, description='Factory ID')
})

@worker_ns.route('/')
class WorkerList(Resource):
    @worker_ns.doc('list_workers', 
                   responses={
                       200: 'Successful retrieval of workers',
                       500: 'Internal server error'
                   })
    @worker_ns.marshal_list_with(worker_model)
    def get(self):
        """List all workers"""
        try:
            workers = Worker.query.all()
            return [w.to_dict() for w in workers]
        except Exception as e:
            abort(500, f'Error retrieving workers: {str(e)}')

    @worker_ns.doc('create_worker', 
                   responses={
                       201: 'Worker created successfully',
                       400: 'Invalid input',
                       404: 'Factory not found',
                       500: 'Internal server error'
                   })
    @worker_ns.expect(worker_input_model)
    @worker_ns.marshal_with(worker_model, code=201)
    def post(self):
        """Create a new worker"""
        try:
            data = request.json
            if not data or 'name' not in data or 'role' not in data or 'factory_id' not in data:
                abort(400, 'Missing required fields')

            # Validate factory exists
            factory = Factory.query.get(data['factory_id'])
            if not factory:
                abort(404, f"Factory with ID {data['factory_id']} not found")

            new_worker = Worker(
                name=data['name'], 
                role=data['role'], 
                factory_id=data['factory_id']
            )
            db.session.add(new_worker)
            db.session.commit()
            return new_worker.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error creating worker: {str(e)}')

@worker_ns.route('/<int:worker_id>')
class WorkerResource(Resource):
    @worker_ns.doc('get_worker', 
                   responses={
                       200: 'Successful retrieval of worker',
                       404: 'Worker not found',
                       500: 'Internal server error'
                   })
    @worker_ns.marshal_with(worker_model)
    def get(self, worker_id):
        """Retrieve a specific worker by ID"""
        try:
            worker = Worker.query.get_or_404(worker_id)
            return worker.to_dict()
        except Exception as e:
            abort(500, f'Error retrieving worker: {str(e)}')

    @worker_ns.doc('update_worker', 
                   responses={
                       200: 'Worker updated successfully',
                       400: 'Invalid input',
                       404: 'Worker not found',
                       500: 'Internal server error'
                   })
    @worker_ns.expect(worker_input_model)
    @worker_ns.marshal_with(worker_model)
    def put(self, worker_id):
        """Update an existing worker"""
        try:
            data = request.json
            if not data or all(key not in data for key in ['name', 'role', 'factory_id']):
                abort(400, 'No update fields provided')

            worker = Worker.query.get_or_404(worker_id)
            
            # Validate factory if provided
            if 'factory_id' in data:
                factory = Factory.query.get(data['factory_id'])
                if not factory:
                    abort(404, f"Factory with ID {data['factory_id']} not found")
                worker.factory_id = data['factory_id']

            # Update other fields if provided
            worker.name = data.get('name', worker.name)
            worker.role = data.get('role', worker.role)
            
            db.session.commit()
            return worker.to_dict()
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error updating worker: {str(e)}')

    @worker_ns.doc('delete_worker', 
                   responses={
                       204: 'Worker deleted successfully',
                       404: 'Worker not found',
                       500: 'Internal server error'
                   })
    def delete(self, worker_id):
        """Delete a worker"""
        try:
            worker = Worker.query.get_or_404(worker_id)
            db.session.delete(worker)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(500, f'Error deleting worker: {str(e)}')