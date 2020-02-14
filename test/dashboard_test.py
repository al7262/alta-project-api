import json
from . import app, client, create_token, db_reset, cache

class TestDashboard():
    # testing display dashboard valid (no params)
    def test_display_outlet_valid_no_params(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?name_outlet=&start_time=&end_time=', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display dashboard valid (start_time & end_time)
    def test_display_outlet_valid_start_end(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?name_outlet=&start_time=01-02-2020&end_time=01-02-2020', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display dashboard invalid (start_time & end_time)
    def test_display_outlet_invalid_start_end(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?name_outlet=&start_time=02-02-2020&end_time=01-02-2020', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    # testing display dashboard valid (name_oulte)
    def test_display_outlet_valid_outlet(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?name_outlet=Surabaya&start_time=&end_time=', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display dashboard valid (all)
    def test_display_outlet_valid_all(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?name_outlet=Surabaya&start_time=01-02-2020&end_time=02-02-2020', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
     # testing display dashboard valid (chart no outlet)
    def test_display_outlet_chart_no_outler(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?name_outlet=&start_time=01-02-2020&end_time=02-02-2020', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing option
    def test_option(self, client):
        # Test the endpoints
        res = client.options('/dashboard')
        assert res.status_code == 200