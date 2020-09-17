class RDS:
    def get_task(id):
        return {'id': id, 'task': 'filler task'}

    def get_all_tasks():
        return {
            'tasks': [
                {'id': 1, 'task': 'filler task 1'},
                {'id': 2, 'task': 'filler task 2'}
            ]
        }

    def create_task(data):
        return {'id': data['id'], 'task': 'not really creating a task, are we'}
