from unittest import TestCase

from challenge.model.job import JobModel


class Test(TestCase):
    def test_result_model(self):
        task = JobModel(task_id=10)
        assert task.task_id == 10
