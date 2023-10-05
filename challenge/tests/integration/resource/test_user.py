class TestUser:
    def test_register(self, client, db):
        response = client.post(
            "/register", json={"username": "admintest", "password": "123"}
        )
        assert response.status_code == 201

    def test_login(self, client, db):
        response = client.post(
            "/register", json={"username": "admintest", "password": "123"}
        )
        assert response.status_code == 201

    def test_logout(self, client, db):
        response = client.post(
            "/register", json={"username": "admintest", "password": "123"}
        )
        assert response.status_code == 201
