import json
from db import DB


def respond(fn, *args):
    try:
        return fn(*args)
    except Exception as e:
        return {
            'error': str(e),
        }

def list_tasks(event, context):
    return respond(DB.get_all_tasks)

def get_task(event, context):
    return respond(DB.get_task, event['path']['task_id'])

def create_task(event, context):
    data = json.loads(event['body'])
    return respond(DB.create_task, data)

