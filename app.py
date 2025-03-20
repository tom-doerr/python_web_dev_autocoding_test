from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)
    app.tasks = []

    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        return jsonify(app.tasks)

    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        task_data = request.get_json()
        task = {
            'id': len(app.tasks) + 1,
            'title': task_data.get('title'),
            'description': task_data.get('description', ''),
            'status': task_data.get('status', 'todo')
        }
        app.tasks.append(task)
        return jsonify(task), 201

    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        task_data = request.get_json()
        if task_id > len(app.tasks) or task_id < 1:
            return jsonify({'error': 'Task not found'}), 404
        task = app.tasks[task_id - 1]
        task.update(task_data)
        return jsonify(task)

    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        if task_id > len(app.tasks) or task_id < 1:
            return jsonify({'error': 'Task not found'}), 404
        del app.tasks[task_id - 1]
        return '', 204

    return app
