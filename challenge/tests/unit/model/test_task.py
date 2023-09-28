from unittest import TestCase

from challenge.model.task import TaskModel


class Test(TestCase):
    def test_item_model(self):
        task = TaskModel(
            name="first",
            url="https://s3-us-west-2.amazonaws.com/eb-python-challenge/php-architecture/salesmeeting2020.json",
            parameters="",
        )

        assert task.name == "first"
        assert (
            task.url
            == "https://s3-us-west-2.amazonaws.com/eb-python-challenge/php-architecture/salesmeeting2020.json"
        )
