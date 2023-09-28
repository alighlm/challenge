from datetime import datetime, timezone

from challenge.model import TaskModel, TaskStatus


def start_task(task: TaskModel):
    task.attempt += 1
    task.fetch_start_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    task.fetch_result = TaskStatus.Started
    task.fetch_end_time = None
    task.save()
    return None


def feed_service():
    valid_tasks = TaskModel.find_all_tasks()

    for task in valid_tasks:
        from challenge.service.fetch_service import fetch_url

        fetch_url.apply_async(
            kwargs={"task_id": task.id, "url": task.url, "parameters": task.parameters},
            time_limit=task.max_execution_time,
            soft_time_limit=task.max_execution_time,
        )

        start_task(task=task)
