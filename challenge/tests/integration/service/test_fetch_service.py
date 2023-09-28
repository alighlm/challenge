import json
from unittest import TestCase

from challenge.model import JobModel, TaskModel
from challenge.model.data import DataModel
from challenge.service.fetch_service import parse


class Test(object):
    def test_parse(self, app, client):
        item = TaskModel(name="test87", url="http://test", parameters="")
        item.save()

        job = JobModel(task_id=item.id)
        job.save()
        json_data = """[
        {
                "id": "bdc3ab3979cb",
                "name_first": "Rhiann",
                "name_last": "Olsen",
                "decription": "Fingerstache unicorn actually, taxidermy try-hard mixtape deep v farm-to-table cardigan pour-over DIY literally keytar vinyl.",
                "title": "Account Manager"
            },
            {
                "id": "0d6b86ea27cd",
                "name_first": "Kamil",
                "name_last": "Hogg",
                "decription": "Mlkshk woke authentic kale chips street art, scenester vape godard iPhone.",
                "title": "Project Manager"
            }
        ]"""

        parse(job_id=job.id, data=json_data)
        assert len(DataModel.query.all()) is 2
