import json
from . import app, client, create_token, db_reset #cache

class TestAuth():
    # Register session test for valid input 
    def test_register_valid(self, client):
        # Prepare the DB
        db_reset()

        # Prepare the data to be inputted
        data = {
            "email": "azzahra@alterra.id",
            "password": "Azzahra1",
        }

        # Test the endpoints
        res = client.post('/user/register', json = data)
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['message'] == 'Registrasi Berhasil'

    # Register session for duplicate email
    def test_register_duplicate_email(self, client):
        # Prepare the data to be inputted
        data = {
            "email": "azzahra@alterra.id",
            "password": "Azzahra1",
        }

        # Test the endpoints
        res = client.post('/user/register', json = data)
        res_json = json.loads(res.data)
        assert res.status_code == 401
        assert res_json['message'] == 'Registrasi Gagal'

    # Register - Password not match the requirement
    def test_register_password_not_match_requirement(self, client):
        # Prepare the data to be inputted
        data = {
            "email": "agung@alterra.id",
            "password": "agung",
        }

        # Test the endpoints
        res = client.post('/user/register', json = data)
        res_json = json.loads(res.data)
        assert res.status_code == 422