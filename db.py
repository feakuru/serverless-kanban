import os
import psycopg2
from psycopg2.extras import DictCursor


class DB:
    @classmethod
    def __connection(cls):
        return psycopg2.connect(
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'], 
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST']
        )
    
    @classmethod
    def __format_task(cls, task):

        def get_status(started, finished):
            if started is None:
                return "To Do"
            elif finished is None:
                return "In Progress"
            else:
                return "Done"

        def get_cost(started, finished):
            if started and finished:
                hours = (finished - started).seconds / 3600
                return hours * int(os.environ.get('TASK_HOURLY_COST', 1000))

        return {
            'id': task['id'],
            'text': task['text'],
            'started': str(task['started']),
            'finished': str(task['finished']),
            'status': get_status(task['started'], task['finished']),
            'cost': get_cost(task['started'], task['finished'])
        }

    @classmethod
    def get_task(cls, task_id):
        with cls.__connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    'SELECT * FROM tasks WHERE id=%s',
                    (task_id, )
                )
                result = cursor.fetchone()
                if result is not None:
                    return cls.__format_task(result)
        raise Exception('Not found!')

    @classmethod
    def get_all_tasks(cls):
        tasks = []
        with cls.__connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    'SELECT * FROM tasks'
                )
                result = cursor.fetchall()
                tasks = [cls.__format_task(row) for row in result]
        return {'tasks': tasks}

    @classmethod
    def create_task(cls, data):
        if 'text' not in data:
            raise Exception('Data should contain text')
        with cls.__connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    'INSERT INTO tasks(text) VALUES (%s) RETURNING id',
                    (data['text'], )
                )
                result_id = cursor.fetchone()['id']
                conn.commit()
                return cls.get_task(result_id)
        raise Exception('Not found!')

    @classmethod
    def start_task(cls, task_id):
        with cls.__connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    'UPDATE tasks SET started=NOW() WHERE id=%s AND started IS NULL',
                    (task_id, )
                )
                conn.commit()
                return {'status': 'ok'}
        raise Exception('DB error')

    @classmethod
    def finish_task(cls, task_id):
        with cls.__connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    'UPDATE tasks SET finished=NOW() WHERE id=%s '
                        + 'AND started IS NOT NULL'
                        + 'AND finished IS NULL',
                    (task_id, )
                )
                conn.commit()
                return {'status': 'ok'}
        raise Exception('DB error')
