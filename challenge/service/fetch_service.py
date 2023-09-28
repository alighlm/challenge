import json
from datetime import timezone, datetime
from typing import List, Dict

import requests

from challenge.app import create_celery_app
from celery.utils.log import get_task_logger

from challenge.model import TaskStatus, JobModel, TaskModel, DataModel

celery = create_celery_app()


logger = get_task_logger(__name__)

result = ["Idle", "Started", "Finished", "Failed"]


def prepair_url(url: str, parameters: Dict[str, str]):
    """
    prepare url, it can be authentication or any thing
    @return:
    """

    return url + parameters["eventfile"]


def parse(job_id: int, data: str):
    objs = json.loads(data)
    for obj in objs:
        DataModel(
            job_id=job_id,
            data_id=obj["id"],
            name_first=obj["name_first"],
            name_last=obj["name_last"],
            decription=obj["decription"],
            title=obj["title"],
        ).save()


def handle_finished_task(task_id: int, status: TaskStatus):
    task = TaskModel.find_by_id(task_id)
    task.fetch_end_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    task.fetch_result = status
    if status == TaskStatus.Finished:
        task.attempt = 0
    task.save()


def handle_finished_job(job: JobModel, status: TaskStatus):
    job.finished_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    job.status = status
    job.save()


@celery.task()
def fetch_url(task_id: int, url: str, parameters: str):
    started_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    job = JobModel(
        task_id=task_id,
        started_time=started_time,
        status=TaskStatus.Started,
    )
    job.save()
    try:
        data = json.loads(parameters)
        encoded = prepair_url(url, data)
        logger.info("running task:{} for url:{}".format(task_id, url))
        response = requests.get(encoded)
        parse(job_id=job.id, data=response.text)

    except Exception as e:
        logger.exception("An error occurred during job:{}".format(job.id))
        handle_finished_job(job, TaskStatus.Failed)
        handle_finished_task(task_id, TaskStatus.Failed)

    else:
        handle_finished_job(job, TaskStatus.Finished)
        handle_finished_task(task_id, TaskStatus.Finished)

    if job.status == TaskStatus.Failed:
        return -1
    return 1
