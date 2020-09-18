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
        return {
            'id': task['id'],
            'text': task['text'],
            'started': task['started'],
            'finished': task['finished'],
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
