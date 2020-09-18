# Serverless Kanban board
This is a simple API for a Kanban board app designed with serverless.com. It is written in Python 3.8. You can test it out at `https://gr2iwhc2al.execute-api.eu-west-1.amazonaws.com/dev/`.

## Methods

### `GET  /tasks/`

Fetches all existing tasks.

Request parameters: none

Response:

```json
{
    "tasks": [
        {
            "id": 5,
            "text": "kek!",
            "started": "None",
            "finished": "None",
            "status": "To Do",
            "cost": null
        },
        {
            "id": 7,
            "text": "kek 2!",
            "started": "2020-09-18 20:12:06.154232",
            "finished": "None",
            "status": "In Progress",
            "cost": null
        },
        {
            "id": 6,
            "text": "kek 2!",
            "started": "2020-09-18 20:11:06.755262",
            "finished": "2020-09-18 20:19:32.493296",
            "status": "Done",
            "cost": 14.027777777777779
        }
    ]
}
```

### `GET  /tasks/{task_id}/`

Fetches task by ID.

Request parameters:

* `task_id` (in path) - id of the task needed. No restrictions are placed on this parameter in order to be able to change ID type at will, but it is Postgres' `serial` in the current scheme.

Response:

```json
{
    "id": 1,
    "text": "Test task",
    "started": "2020-09-18 20:11:06.755262",
    "finished": "2020-09-18 20:19:32.493296",
    "status": "Done",
    "cost": 12
}
```

Or:

```json
{
    "error": "Not found!"
}
```

### `POST /tasks/`

Creates a task. Ignores every field except "text".

Request format:

```json
{
    "text": "123"
}
```

Response:

```json
{
    "id": 1,
    "text": "Test task",
    "started": "2020-09-18 20:11:06.755262",
    "finished": "2020-09-18 20:19:32.493296",
    "status": "Done",
    "cost": 12
}
```

### `GET  /tasks/{task_id}/start/`

Sets task's `started` field to now if it is not set. No way to cancel this!

Request parameters: 

* `task_id` (in path) - id of the task needed. No restrictions are placed on this parameter in order to be able to change ID type at will, but it is Postgres' `serial` in the current scheme.

Response:
```json
{
    "status": "ok"
}
```

### `GET  /tasks/{task_id}/finish/`

Sets task's `finished` field to now if it is not set and `started` is set. No way to cancel this!

Request parameters:

* `task_id` (in path) - id of the task needed. No restrictions are placed on this parameter in order to be able to change ID type at will, but it is Postgres' `serial` in the current scheme.

Response:
```json
{
    "status": "ok"
}
```
