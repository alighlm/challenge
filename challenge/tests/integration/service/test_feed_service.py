from datetime import timezone, datetime, timedelta

from challenge.model import TaskModel, JobModel, TaskStatus


class TestTask(object):
    def test_feed_service_task_finished_more_than_interval(self, client, db):
        # senario 1 task a finished in more than interval
        task = TaskModel(
            name="test_feed_service_task_finished_more_than_interval",
            url="http://test",
            parameters="",
            start_time=(datetime.utcnow() - timedelta(days=10)).replace(
                tzinfo=timezone.utc
            ),
            end_time=(datetime.utcnow() + timedelta(days=30)).replace(
                tzinfo=timezone.utc
            ),
            fetch_start_time=(datetime.utcnow() - timedelta(seconds=100)).replace(
                tzinfo=timezone.utc
            ),
            fetch_end_time=(datetime.utcnow() - timedelta(seconds=50)).replace(
                tzinfo=timezone.utc
            ),
            task_interval=20,
            fetch_result=TaskStatus.Finished,
        )
        task.save()

        valid_tasks = TaskModel.find_all_current_valid_less_than_interval().all()

        assert len(valid_tasks) == 1
        assert valid_tasks[0].id == task.id

    def test_feed_service_task_finished_less_than_interval(self, client, db):
        task = TaskModel(
            name="test4",
            url="http://test",
            parameters="",
            start_time=(datetime.utcnow() - timedelta(days=10)).replace(
                tzinfo=timezone.utc
            ),
            end_time=(datetime.utcnow() + timedelta(days=30)).replace(
                tzinfo=timezone.utc
            ),
            fetch_start_time=(datetime.utcnow() - timedelta(seconds=5)).replace(
                tzinfo=timezone.utc
            ),
            fetch_end_time=(datetime.utcnow()).replace(tzinfo=timezone.utc),
            task_interval=10,
            fetch_result=TaskStatus.Finished,
        )
        task.save()

        valid_tasks = TaskModel.find_all_current_valid_less_than_interval().all()
        assert len(valid_tasks) == 0

    def test_feed_service_task_new(self, client, db):
        # senario 3 task has not any job record
        valid_tasks = TaskModel.find_all_current_valid_new().all()
        assert len(valid_tasks) == 0

        task = TaskModel(
            name="test5",
            url="http://test",
            parameters="",
            start_time=(datetime.utcnow() - timedelta(days=10)).replace(
                tzinfo=timezone.utc
            ),
            end_time=(datetime.utcnow() + timedelta(days=30)).replace(
                tzinfo=timezone.utc
            ),
            task_interval=10,
        )
        task.save()

        valid_tasks = TaskModel.find_all_current_valid_new().all()
        assert len(valid_tasks) == 1

    def test_failed_jobs(self, client, db):
        task = TaskModel(
            name="test4",
            url="http://test",
            parameters="",
            start_time=(datetime.utcnow() - timedelta(days=10)).replace(
                tzinfo=timezone.utc
            ),
            end_time=(datetime.utcnow() + timedelta(days=30)).replace(
                tzinfo=timezone.utc
            ),
            fetch_start_time=(datetime.utcnow() - timedelta(seconds=5)).replace(
                tzinfo=timezone.utc
            ),
            fetch_end_time=(datetime.utcnow()).replace(tzinfo=timezone.utc),
            task_interval=10,
            fetch_result=TaskStatus.Failed,
            attempt=1,
            max_attempt=5,
        )
        task.save()
        valid_tasks = TaskModel.find_all_lasttime_failed().all()
        assert len(valid_tasks) == 1
