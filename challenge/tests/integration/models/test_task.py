from datetime import datetime, timezone, timedelta

from challenge.model.job import JobModel, TaskStatus
from challenge.model.task import TaskModel


class TestTask(object):
    def test_task_model(self, client, db):
        item = TaskModel(name="test-1", url="http://test", parameters="")

        assert TaskModel.find_by_name("test-1") is None

        item.save()
        assert TaskModel.find_by_name("test-1") is not None

        item.delete()
        assert TaskModel.find_by_name("test-1") is None

    def test_insert_task_result_model(self, client, db):
        item = TaskModel(name="test", url="http://test", parameters="")
        item.save()

        assert TaskModel.find_by_name("test") is not None

        result = JobModel(task_id=item.id)
        result.save()
        result = JobModel.find_by_task_id(item.id)

        assert result is not None
        assert result.status is TaskStatus.Idle
        assert result.status is not TaskStatus.Started

    def test_job_started(self, client, db):
        item = TaskModel(name="test", url="http://test", parameters="")
        item.save()

        result = JobModel(task_id=item.id)
        result.save()
        result.job_started()

        db_result = JobModel.find_by_task_id(item.id)
        assert db_result is not None
        assert db_result.status is TaskStatus.Started

    def test_job_finished(self, client, db):
        item = TaskModel(name="test87", url="http://test", parameters="")
        item.save()

        result = JobModel(task_id=item.id)
        result.save()
        result.job_finished(TaskStatus.Failed, "")

        db_result = JobModel.find_by_task_id(item.id)
        assert db_result is not None
        assert db_result.status is TaskStatus.Failed

        result.job_finished(TaskStatus.Finished, "{}")
        db_result = JobModel.find_by_task_id(item.id)

        assert db_result is not None
        assert db_result.status is TaskStatus.Finished
        assert db_result.response == "{}"
