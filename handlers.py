import json
from rds import RDS


def respond(fn, *args):
    try:
        return {
            'statusCode': 200,
            'body': json.dumps(fn(*args))
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': {
                'error': str(e)
            }
        }

def list_tasks(event, context):
    return respond(RDS.get_all_tasks)

def get_task(event, context):
    return respond(RDS.get_task, event['path']['task_id'])

def create_task(event, context):
    data = json.loads(event['body'])
    return respond(RDS.create_task, data)

