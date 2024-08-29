from flask import request, jsonify
from app import db
from models import Task

def init_routes(app):
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.serialize() for task in tasks])

    @app.route('/tasks', methods=['POST'])
    def create_task():
        data = request.get_json()
        new_task = Task(title=data['title'], description=data.get('description'))
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.serialize()), 201

    @app.route('/tasks/<int:id>', methods=['PUT'])
    def update_task(id):
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        data = request.get_json()
        task.title = data['title']
        task.description = data.get('description')
        task.done = data.get('done', task.done)
        db.session.commit()
        return jsonify(task.serialize())

    @app.route('/tasks/<int:id>', methods=['DELETE'])
    def delete_task(id):
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})
