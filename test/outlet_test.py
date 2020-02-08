import json
from . import app, client, create_token, db_reset, cache

class TestOutlet():
    # testing display outlet valid (with keyword)
    def test_display_outlet_valid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/outlet?p=1&rp=25&keyword=Surabaya', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display outlet valid (without keyword)
    def test_display_outlet_valid_without_keyword(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/outlet?p=1&rp=25', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing delete outlet valid
    def test_delete_outlet_valid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.delete('/outlet/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        db_reset()

    # testing delete outlet invalid
    def test_delete_outlet_invalid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.delete('/outlet/1', headers={'Authorization': 'Bearer ' + token})
        res = client.delete('/outlet/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        db_reset()
    
    # testing edit outlet valid
    def test_edit_outlet_valid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        #data input
        data = {
            "name": "Hedy Gading",
            "phone_number": "081411231009",
            "address": "Jl. kupang",
            "city": "Surabaya",
            "tax": 15
        }

        # Test the endpoints
        res = client.put('/outlet/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing edit outlet invalid
    def test_edit_outlet_invalid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        #data input
        data = {
            "name": "Hedy Gading",
            "phone_number": "081411231009",
            "address": "Jl. kupang",
            "city": "Surabaya",
            "tax": 15
        }

        # Test the endpoints
        res = client.delete('/outlet/1', headers={'Authorization': 'Bearer ' + token})
        res = client.put('/outlet/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
        db_reset()


    # testing create outlet valid
    def test_create_outlet_valid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        #data input
        data = {
            "name": "Bandung",
            "phone_number": "081411231009",
            "address": "Jl. kupang",
            "city": "Surabaya",
            "tax": 15
        }

        # Test the endpoints
        res = client.post('/outlet/create', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # testing display outlet by one valid
    def test_display_outlet_by_one_valid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/outlet/get/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display outlet by one invalid
    def test_display_outlet_by_one_invalid(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.delete('/outlet/1', headers={'Authorization': 'Bearer ' + token})
        res = client.get('/outlet/get/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404