from flask_jwt_extended import create_access_token


class TestTask(object):
    def test_save_new_task(self, client):
        access_token = create_access_token(
            identity=1,
            expires_delta=False,
            fresh=True,
            additional_claims={"is_administrator": True},
        )
        headers = {"Authorization": "Bearer {}".format(access_token)}
        response = client.post(
            "/tasks",
            json={
                "name": "task1",
                "url": "https://s3-us-west-2.amazonaws.com/eb-python-challenge/php-architecture/amazingexpo2020.json",
                "parameters": "{}",
                "start_time": "2023-01-04T21:41:38.930Z",
                "end_time": "2023-12-04T21:41:38.930Z",
                "task_interval": 10,
                "max_execution_time": 0,
                "max_attempt": 10,
            },
            headers=headers,
        )
        assert response.status_code == 201
        response = client.get(
            "/tasks",
            headers=headers,
        )

        assert response.status_code == 200
        assert b"url" in response.data

    def test_status_a_task(self, client):
        access_token = create_access_token(
            identity=1,
            expires_delta=False,
            fresh=True,
            additional_claims={"is_administrator": True},
        )
        headers = {"Authorization": "Bearer {}".format(access_token)}
        response = client.get(
            "/tasks/1/status",
            headers=headers,
        )
        assert response.status_code == 200

    def test_rest_attempt_a_task(self, client):
        access_token = create_access_token(
            identity=1,
            expires_delta=False,
            fresh=True,
            additional_claims={"is_administrator": True},
        )
        headers = {"Authorization": "Bearer {}".format(access_token)}
        response = client.post(
            "/tasks/1/reset-attempt",
            headers=headers,
        )
        assert response.status_code == 200

    def test_delete_a_task(self, client):
        access_token = create_access_token(
            identity=1,
            expires_delta=False,
            fresh=True,
            additional_claims={"is_administrator": True},
        )
        headers = {"Authorization": "Bearer {}".format(access_token)}
        response = client.delete(
            "/tasks/1",
            headers=headers,
        )
        assert response.status_code == 200
