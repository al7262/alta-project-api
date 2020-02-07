import json
from . import app, client, cache, create_token, db_reset

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
        res = client.post('/register', json = data)
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['message'] == 'Selamat! Akunmu sudah terdaftar sekarang'